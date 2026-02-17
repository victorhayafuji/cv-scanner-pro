from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.config import Config
from src.models import PerfilCandidato, AnaliseGap, CVOtimizado, AnaliseCurriculoBI  # <--- Importe o novo modelo
from datetime import datetime


class AIEngine:
    def __init__(self):
        # Motor Local (HuggingFace) para evitar erros de API
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Cérebro (Gemini)
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            temperature=0.0,  # <-- AQUI: Zero absoluto para consistência analítica
            google_api_key=Config.GOOGLE_API_KEY,
            max_retries=3 # Aproveitando para manter a blindagem contra erros 503
        )

    def analisar_documentos(self, splits, texto_vaga=None):
        vector_store = FAISS.from_documents(splits, self.embeddings)
        retriever = vector_store.as_retriever(search_kwargs={"k": 7})

        query = "experiência projetos impacto ferramentas datas"
        if texto_vaga:
            query += f" {texto_vaga[:300]}"

        docs = retriever.invoke(query)
        contexto = "\n\n".join([d.page_content for d in docs])

        if texto_vaga:
            return self._executar_gap_analysis(contexto, texto_vaga)
        else:
            return self._executar_extracao_perfil(contexto)

    # --- NOVA FUNÇÃO QUE ESTAVA FALTANDO ---
    def otimizar_cv(self, splits, vaga=None):
        # 1. Recupera o Contexto
        vector_store = FAISS.from_documents(splits, self.embeddings)
        docs = vector_store.as_retriever(search_kwargs={"k": 4}).invoke("experiência profissional projetos resumo")
        contexto = "\n\n".join([d.page_content for d in docs])

        # 2. Define a Data Dinâmica (Isso faltava!)
        data_hoje = datetime.now().strftime("%d de %B de %Y")

        parser = JsonOutputParser(pydantic_object=CVOtimizado)

        # 3. Prompt com Consciência Temporal
        prompt_template = """
        Você é um Especialista em Carreira e "Ghostwriter" Sênior.

        CONTEXTO TEMPORAL (CRÍTICO):
        Hoje é dia: {data_hoje}
        Use esta data para validar se as experiências são atuais, passadas ou futuras.

        FASE 1: A OTIMIZAÇÃO (Copywriting)
        Reescreva o perfil para torná-lo de ALTO IMPACTO.
        - Use método STAR e verbos de ação.
        - Invente placeholders numéricos ([X]%) onde faltar métrica.

        FASE 2: O REALITY CHECK (Auditoria)
        Analise o texto gerado vs. Original.
        - Identifique exageros de senioridade.
        - DATAS: Compare rigorosamente com a data de hoje ({data_hoje}).
          - Se a data do CV for ANTERIOR a hoje, NÃO marque como erro de "data futura".
          - Se a data do CV for POSTERIOR a hoje (Futuro): Alerte APENAS se não houver indicação de "Início Confirmado".

        CONTEXTO ORIGINAL:
        {contexto}

        VAGA ALVO:
        {vaga}

        FORMATO JSON:
        {format_instructions}
        """

        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm | parser

        # 4. Injeta a data na execução
        return chain.invoke({
            "contexto": contexto,
            "vaga": vaga if vaga else "Genérica de Dados",
            "data_hoje": data_hoje,  # <--- A correção está aqui
            "format_instructions": parser.get_format_instructions()
        })

    def _executar_extracao_perfil(self, contexto):
        parser = JsonOutputParser(pydantic_object=PerfilCandidato)
        data_hoje = datetime.now().strftime("%B de %Y")
        prompt = ChatPromptTemplate.from_template(
            """Você é um CTO e Headhunter rigoroso. Analise o CV abaixo.
            DATA DE HOJE: {data_hoje}
            1. CÁLCULO DE EXPERIÊNCIA: Some apenas períodos em tecnologia. Resultado: "X anos e Y meses".
            2. SCORING (0-100): Penalize falta de métricas e clichês.
            3. PERGUNTAS: Gere 3 perguntas técnicas.
            CV: {contexto}
            JSON: {format_instructions}"""
        )
        chain = prompt | self.llm | parser
        return chain.invoke(
            {"contexto": contexto, "data_hoje": data_hoje, "format_instructions": parser.get_format_instructions()})

    def _executar_gap_analysis(self, contexto, vaga):
        parser = JsonOutputParser(pydantic_object=AnaliseGap)
        data_hoje = datetime.now().strftime("%B de %Y")
        
        # Função auxiliar para arredondar para o múltiplo de 5 mais próximo
        def arredondar_5(valor):
            return int(5 * round(float(valor) / 5))

        prompt = ChatPromptTemplate.from_template(
            """Você é um auditor técnico. Sua tarefa é avaliar o CV contra a VAGA e atribuir notas parciais.
            
            HOJE É: {data_hoje}.
            
            REGRAS DE PONTUAÇÃO (RETORNE APENAS MÚLTIPLOS DE 5):
            1. score_tecnico (0-50): Avalie Hard Skills.
            2. score_senioridade (0-30): Avalie se o cargo/tempo bate com a vaga.
            3. score_diferencial (0-20): Avalie extras e diferenciais pedidos.
            
            IMPORTANTE: Use apenas valores como 0, 5, 10, 15, 20, 25, 30...
            
            VAGA: {vaga}
            CV: {contexto}
            JSON: {format_instructions}"""
        )
        
        chain = prompt | self.llm | parser
        res = chain.invoke({
            "contexto": contexto, 
            "vaga": vaga, 
            "data_hoje": data_hoje, 
            "format_instructions": parser.get_format_instructions()
        })

        # --- BLINDAGEM MATEMÁTICA (ARREDONDAMENTO E SOMA) ---
        res["score_tecnico"] = arredondar_5(res.get("score_tecnico", 0))
        res["score_senioridade"] = arredondar_5(res.get("score_senioridade", 0))
        res["score_diferencial"] = arredondar_5(res.get("score_diferencial", 0))

        res["match_percentual"] = (
            res["score_tecnico"] + 
            res["score_senioridade"] + 
            res["score_diferencial"]
        )
        
        return res

    def converter_para_bi(self, dados_gap: dict, nome: str, cargo: str) -> dict:
        """
        Adapta o dicionário de AnaliseGap para o formato flat do BI (AnaliseCurriculoBI).
        """
        # Lógica de inferência para campos faltantes
        score = dados_gap.get("match_percentual", 0)
        
        # Inferência simples de senioridade baseada no score (pode ser melhorada com IA se quiser)
        if score >= 85:
            senioridade = "Senior/Especialista"
        elif score >= 60:
            senioridade = "Pleno"
        else:
            senioridade = "Junior/Iniciante"

        # Converte listas para strings (embora o validator do Pydantic já faça isso na instanciação,
        # aqui preparamos o dicionário para ser compatível antes mesmo da validação ou para o dict final)
        skills = ", ".join(dados_gap.get("pontos_fortes", []))
        gaps = ", ".join(dados_gap.get("gaps_tecnicos", []))

        # Cria o objeto Pydantic para validar e depois exportar como dict
        analise_bi = AnaliseCurriculoBI(
            nome_candidato=nome,
            cargo_alvo=cargo,
            score_aderencia=score,
            nivel_senioridade=senioridade,
            principais_skills=skills,
            gaps_identificados=gaps,
            parecer_resumido=dados_gap.get("analise_comparativa", "")[:500] # Limita tamanho
        )
        
        return analise_bi.model_dump()