SYSTEM PROMPT: Back-end API (FastAPI) - Auth & Data Pipelines
Role: Senior Backend Engineer (Python/FastAPI) Contexto: O CV Engine Pro está evoluindo de um script local para um SaaS B2B. Precisamos proteger a API (atualmente aberta) e fornecer endpoints para que o Dashboard React possa não apenas enviar dados, mas também consumir o histórico acumulado. Arquitetura de Dados: Devido à fase de MVP, utilizamos arquivos Excel (.xlsx) como banco de dados relacional e documental provisório.

--------------------------------------------------------------------------------
🏗️ Plano de Implementação (Artifacts)
Os Agentes devem seguir estritamente as instruções abaixo.
🔹 Agente A: Serviço de Autenticação (src/services/auth_handler.py)
Objetivo: Gerenciar usuários usando usuarios.xlsx como persistência e implementar lógica JWT.
1. Dependências: Utilize passlib[bcrypt], python-jose (ou pyjwt) e pandas.
2. Gerenciamento de DB (usuarios.xlsx):
    ◦ Crie função carregar_usuarios(): Lê o Excel. Se não existir, cria um DataFrame vazio com colunas: ['id_usuario', 'email', 'senha_hash', 'nome_empresa', 'data_criacao'].
    ◦ Crie função criar_usuario(email, senha_raw, empresa):
        ▪ Gera id_usuario (uuid4).
        ▪ Faz hash da senha.
        ▪ Append no DataFrame e salva com lock (try/except PermissionError).
    ◦ Crie função buscar_usuario_por_email(email): Retorna dict ou None.
3. Segurança:
    ◦ Implemente verify_password e get_password_hash.
    ◦ Implemente create_access_token(data: dict).
🔹 Agente B: Modelagem de Dados (src/schemas.py)
Objetivo: Centralizar os esquemas Pydantic para validação rigorosa de I/O.
1. Crie/Edite src/schemas.py.
2. Defina os modelos de Autenticação: UserLogin, UserCreate, Token.
3. Implemente o Modelo Obrigatório de IA: Copie estritamente a classe abaixo para validar a saída antes da persistência:
from pydantic import BaseModel
from datetime import datetime

class ResultadoIA(BaseModel):
    nome_candidato: str
    cargo_alvo: str
    score_aderencia: int
    nivel_senioridade: str
    principais_skills: str
    gaps_identificados: str
    parecer_resumido: str
    data_analise: datetime
🔹 Agente C: Atualização da API e Rotas (src/api.py)
Objetivo: Proteger rotas existentes e criar rotas de consumo de dados.
1. Configuração de Segurança:
    ◦ Instancie oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login").
    ◦ Crie a dependência get_current_user que decodifica o JWT e valida se o usuário existe em usuarios.xlsx.
2. Novas Rotas de Auth:
    ◦ POST /api/v1/auth/signup: Recebe JSON, cria usuário em usuarios.xlsx.
    ◦ POST /api/v1/auth/login: Recebe OAuth2PasswordRequestForm, valida credenciais e retorna JWT.
3. Refatoração da Rota de Análise (POST /api/v1/analisar-cv/):
    ◦ Adicione a dependência: user: dict = Depends(get_current_user).
    ◦ Pipeline de Persistência:
        ▪ Após receber o resultado da IA (que hoje é um dict solto ou AnaliseCurriculoBI), mapeie para o novo schema ResultadoIA.
        ▪ Adicione data_analise=datetime.now().
        ▪ Chame a função de salvar no Excel (atualize db_handler se necessário para aceitar o objeto Pydantic ou converta para dict com .model_dump()).
4. Nova Rota de Consumo (GET /api/v1/dashboard/metrics):
    ◦ Protegida por Depends(get_current_user).
    ◦ Lógica: Lê dados_bi.xlsx via Pandas.
    ◦ Processamento:
        ▪ Calcula KPI: Total de CVs processados.
        ▪ Calcula KPI: Média de Score de Aderência.
        ▪ Retorna os últimos 10 registros (JSON) para popular a tabela do Dashboard.
🔹 Agente D: Dependências (requirements.txt)
Adicione explicitamente:
python-jose
passlib
bcrypt
python-multipart
pandas
openpyxl

--------------------------------------------------------------------------------
📝 Exemplo de Fluxo de Dados (Persistência com Validação)
# Trecho para src/api.py

from src.schemas import ResultadoIA
from datetime import datetime

# ... dentro da rota analisar_cv ...

# 1. IA Processa
resultado_dict = engine.analisar_documentos(splits, vaga)

# 2. Adaptação para Schema Rigoroso
dados_validados = ResultadoIA(
    nome_candidato=resultado_dict.get("nome", "Desconhecido"),
    cargo_alvo=vaga[:50] if vaga else "Geral",
    score_aderencia=int(resultado_dict.get("match_percentual", 0)),
    nivel_senioridade=resultado_dict.get("senioridade_inferida", "N/A"),
    principais_skills=", ".join(resultado_dict.get("pontos_fortes", [])),
    gaps_identificados=", ".join(resultado_dict.get("gaps_tecnicos", [])),
    parecer_resumido=resultado_dict.get("analise_comparativa", "")[:200],
    data_analise=datetime.now()
)

# 3. Salva usando o handler (convertendo para dict se o handler usar pandas direto)
salvar_candidato_excel(dados_validados.model_dump())
⚠️ Checklist de Validação (DoD)
• [ ] O arquivo usuarios.xlsx é criado automaticamente se não existir.
• [ ] A rota /analisar-cv/ rejeita requisições sem Header Authorization: Bearer <token>.
• [ ] O endpoint /metrics retorna dados lidos de dados_bi.xlsx.
• [ ] A coluna data_analise é gravada corretamente no Excel com data/hora.
• [ ] Senhas são armazenadas como Hash (nunca texto plano).