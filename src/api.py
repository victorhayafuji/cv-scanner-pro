from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import pandas as pd
import os

from src.services.ai_engine import AIEngine
from src.services.pdf_handler import processar_pdf
from src.services.db_handler import salvar_candidato_excel
from src.services.auth_handler import (
    criar_usuario, buscar_usuario_por_email, verify_password, 
    create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)
from src.schemas import UserCreate, Token, ResultadoIA

app = FastAPI(title="CV Engine Pro API", version="1.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SEGURANÇA ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Decodifica o token e valida se o usuário existe."""
    from jose import JWTError, jwt
    from src.services.auth_handler import SECRET_KEY, ALGORITHM

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = buscar_usuario_por_email(email)
    if user is None:
        raise credentials_exception
    return user

# --- ROTAS DE AUTENTICAÇÃO ---

@app.post("/api/v1/auth/signup", response_model=dict)
async def signup(user: UserCreate):
    usuario_existente = buscar_usuario_por_email(user.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    
    criar_usuario(user.email, user.password, user.nome_empresa)
    return {"message": "Usuário criado com sucesso!"}

@app.post("/api/v1/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = buscar_usuario_por_email(form_data.username)
    if not usuario or not verify_password(form_data.password, usuario['senha_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/auth/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "email": current_user["email"],
        "empresa": current_user.get("empresa", "")
    }

# --- ROTAS DE NEGÓCIO ---

@app.post("/api/v1/analisar-cv/")
async def analisar_cv(
    arquivo: UploadFile = File(...), 
    vaga: str = Form(None),
    current_user: dict = Depends(get_current_user) # Rota protegida
):
    try:
        # 1. Processamento do PDF
        splits = processar_pdf(arquivo.file)
        if not splits:
            raise HTTPException(status_code=400, detail="O arquivo parece ser uma imagem ou está vazio. Por favor, envie um PDF com texto selecionável.")

        # 2. Motor de IA
        engine = AIEngine()
        resultado = engine.analisar_documentos(splits, vaga)

        # 3. Persistência com Validação de Schema (Apenas se houver vaga)
        if vaga:
            try:
                # Normalização de nomes
                nome_arquivo_limpo = arquivo.filename.replace(".pdf", "").replace("_", " ").title() if arquivo.filename else "Candidato Desconhecido"
                
                # Instancia o Schema Pydantic para validar os tipos
                dados_validados = ResultadoIA(
                    nome_candidato=resultado.get("nome", nome_arquivo_limpo),
                    cargo_alvo=vaga[:50] + "..." if len(vaga) > 50 else vaga,
                    score_aderencia=int(resultado.get("match_percentual", 0)),
                    nivel_senioridade=resultado.get("senioridade_inferida", resultado.get("senioridade", "N/A")), # Tenta pegar senioridade se IA retornar
                    principais_skills=", ".join(resultado.get("pontos_fortes", [])),
                    gaps_identificados=", ".join(resultado.get("gaps_tecnicos", [])),
                    parecer_resumido=resultado.get("analise_comparativa", "")[:500],
                    data_analise=datetime.now()
                )

                # Salva usando o handler existente (que espera listas flatten ou dict)
                # O metodo db_handler.salvar_candidato_excel espera um dict com chaves específicas
                # Vamos converter o modelo para dict compatível com o db_handler atual
                # Nota: O db_handler.salvar_candidato_excel espera chaves específicas do AnaliseCurriculoBI
                # Para evitar quebrar o db_handler agora, vamos usar o converter_para_bi do engine mas injetando a data
                
                # A função engine.converter_para_bi já faz o flat. Vamos usar ela.
                dados_bi = engine.converter_para_bi(resultado, dados_validados.nome_candidato, vaga)
                
                # Injeta data_analise que não existe originalmente no AnaliseCurriculoBI antigo (se existir)
                dados_bi['data_analise'] = dados_validados.data_analise.strftime("%Y-%m-%d %H:%M:%S")
                
                salvar_candidato_excel(dados_bi)

            except Exception as e:
                print(f"Erro ao salvar BI: {e}")
                # Não falha a request se o log der erro, mas loga

        return resultado

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@app.get("/api/v1/dashboard/metrics")
async def dashboard_metrics(current_user: dict = Depends(get_current_user)): # Protegido
    """Retorna KPIs e histórico recente para o Dashboard."""
    CAMINHO_EXCEL = "dados_bi.xlsx"
    
    if not os.path.exists(CAMINHO_EXCEL):
        return {
            "total_cvs": 0,
            "media_score": 0,
            "recent_activity": []
        }
    
    try:
        df = pd.read_excel(CAMINHO_EXCEL)
        
        # KPIs
        total_cvs = len(df)
        media_score = int(df['score_aderencia'].mean()) if not df.empty else 0
        
        # Histórico Completo para Analytics (Client-Side Aggregation)
        # Garante que data_analise esteja em string ISO para o front
        if 'data_analise' in df.columns:
            # Converte colunas de data que possam estar como objeto/datetime
            df['data_analise'] = df['data_analise'].astype(str)
            
        df = df.fillna("")
        
        # Retorna lista completa para cálculos no front (Charts, Filtros de Data)
        all_records = df.to_dict(orient="records")
        
        # Mantém compatibilidade com o dashboard antigo (recent_activity)
        recent_activity = df.tail(10).iloc[::-1].to_dict(orient="records")
        
        return {
            "total_cvs": total_cvs,
            "media_score": media_score,
            "recent_activity": recent_activity,
            "all_records": all_records # Novo campo para o Analytics Dashboard
        }
    except Exception as e:
        print(f"Erro ao ler dashboard: {e}")
        raise HTTPException(status_code=500, detail="Erro ao carregar dados do dashboard.")
