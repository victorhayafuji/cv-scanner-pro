SYSTEM PROMPT: Arquitetura de API REST (FastAPI)
Role: Lead Software Architect Contexto: O CV Engine Pro opera atualmente como um monólito acoplado à interface visual (dashboard.py). Para permitir integrações externas (Web/Mobile), precisamos expor a lógica de negócios (AIEngine, pdf_handler, db_handler) através de uma API RESTful robusta.
Objetivo: Implementar src/api.py utilizando FastAPI, reutilizando os serviços existentes e garantindo que o sistema atual (Streamlit) continue funcionando.

--------------------------------------------------------------------------------
🏗️ Plano de Implementação (Artifacts)
Os Agentes devem seguir estritamente as instruções abaixo para modificar e criar os arquivos necessários.
🔹 Agente A: Infraestrutura da API (src/api.py)
Objetivo: Configurar o servidor e as regras de segurança (CORS).
1. Crie o arquivo src/api.py.
2. Importe FastAPI e CORSMiddleware.
3. Instancie o app com metadados: title="CV Engine Pro API", version="1.0".
4. Configuração de CORS:
    ◦ Adicione o middleware CORSMiddleware.
    ◦ Defina allow_origins=["*"] (Crítico para permitir requisições de front-ends externos).
    ◦ Defina allow_credentials=True, allow_methods=["*"], allow_headers=["*"].
🔹 Agente B: Roteamento e Orquestração (src/api.py)
Objetivo: Criar o endpoint principal que conecta o Upload -> OCR -> AI -> Banco de Dados.
1. Importações:
    ◦ UploadFile, File, Form, HTTPException do fastapi.
    ◦ Serviços do projeto: src.services.ai_engine (Classe AIEngine), src.services.pdf_handler (processar_pdf) e src.services.db_handler (salvar_candidato_excel).
2. Criação da Rota:
    ◦ Verbo/Caminho: POST /api/v1/analisar-cv/.
    ◦ Parâmetros: arquivo: UploadFile, vaga: str = Form(None).
3. Lógica de Execução (Fluxo):
    ◦ Passo 1 (Adaptação de Arquivo): O serviço processar_pdf existente espera um objeto que tenha o método .read(). O UploadFile do FastAPI possui o atributo .file que atende a isso. Passe arquivo.file para o processar_pdf.
        ▪ Check de Segurança: Se processar_pdf retornar None ou lista vazia, levante HTTPException(400, "Erro ao processar PDF").
    ◦ Passo 2 (IA):
        ▪ Instancie engine = AIEngine().
        ▪ Chame resultado = engine.analisar_documentos(splits, vaga).
    ◦ Passo 3 (Persistência BI):
        ▪ Verifique if vaga:.
        ▪ Extraia o nome do candidato do resultado (resultado.get("nome")) ou use o nome do arquivo (arquivo.filename).
        ▪ Utilize o método engine.converter_para_bi(resultado, nome, vaga).
        ▪ Chame salvar_candidato_excel(dados_bi).
    ◦ Passo 4 (Retorno): Retorne o dicionário resultado como JSON.
4. Tratamento de Erros: Envolva todo o bloco lógico em um try/except. Retorne código 500 para erros genéricos.
🔹 Agente C: Gerenciamento de Dependências (requirements.txt)
Objetivo: Garantir que o ambiente suporte o servidor web e a manipulação de dados.
1. Edite o arquivo requirements.txt.
2. Adicione as seguintes bibliotecas essenciais para a nova arquitetura:
3. (Nota: pandas e openpyxl já são usados no db_handler, mas precisam estar explícitos no requirements para o deploy da API).

--------------------------------------------------------------------------------
📝 Exemplo de Estrutura de Código (src/api.py)
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.services.ai_engine import AIEngine
from src.services.pdf_handler import processar_pdf
from src.services.db_handler import salvar_candidato_excel

app = FastAPI(title="CV Engine Pro API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/analisar-cv/")
def analisar_cv(arquivo: UploadFile = File(...), vaga: str = Form(None)):
    try:
        # 1. Processamento do PDF
        # O pdf_handler [1] lê o arquivo, cria um temp e faz o split
        splits = processar_pdf(arquivo.file)
        
        if not splits:
            raise HTTPException(status_code=400, detail="Não foi possível ler o PDF ou ele está vazio.")

        # 2. Motor de IA
        engine = AIEngine()
        resultado = engine.analisar_documentos(splits, vaga)

        # 3. Persistência (Regra de Negócio: Só salva no BI se houver Vaga para comparar)
        if vaga:
            try:
                # Recupera nome do JSON ou usa o nome do arquivo
                nome_candidato = resultado.get("nome", arquivo.filename.replace(".pdf", "").replace("_", " ").title())
                
                # Usa o conversor existente na classe AIEngine [3]
                dados_bi = engine.converter_para_bi(resultado, nome_candidato, vaga)
                
                salvar_candidato_excel(dados_bi)
            except Exception as e:
                # Log de erro silencioso para não falhar a request principal
                print(f"Erro ao salvar BI: {e}")

        return resultado

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
⚠️ Checklist de Validação (DoD)
• [ ] O comando uvicorn src.api:app --reload inicia a API sem erros.
• [ ] A rota aceita upload via Swagger UI (/docs).
• [ ] O arquivo Excel é atualizado automaticamente quando uma vaga é enviada.
• [ ] requirements.txt contém python-multipart (necessário para UploadFile).
• [ ] Nenhuma alteração foi feita dentro de src/services/ai_engine.py ou src/services/pdf_handler.py que pudesse quebrar o Streamlit.