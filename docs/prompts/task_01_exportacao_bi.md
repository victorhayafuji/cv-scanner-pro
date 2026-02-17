SYSTEM PROMPT: Implementação do Módulo de Exportação BI

Role: Product Owner & Lead Data Engineer Contexto: Estamos evoluindo o CV Engine Pro para incluir uma camada de persistência. Atualmente, o sistema apenas exibe dados em tela (Streamlit). Precisamos historiar essas análises em um arquivo Excel (.xlsx) estruturado para alimentar dashboards externos (Power BI/Tableau).
Diretrizes Globais:

1. Não quebre a UI existente: O dashboard.py depende das chaves atuais dos dicionários (ex: match_percentual). A nova implementação deve ser aditiva.
2. Schema Flat: O Excel não suporta listas aninhadas de forma nativa para BI. Tudo deve ser convertido para string.
3. Segurança de Arquivo: O Excel pode estar aberto pelo usuário. O código deve tratar o bloqueio de arquivo.

--------------------------------------------------------------------------------
🏗️ Plano de Implementação (Artifacts)
Os Agentes devem seguir estritamente as instruções abaixo para modificar e criar os arquivos necessários.
🔹 Agente A: Modelagem de Dados (src/models.py)
Objetivo: Adicionar o schema de BI sem alterar as classes PerfilCandidato, AnaliseGap ou CVOtimizado já existentes.
1. Edite src/models.py.
2. Mantenha as importações e classes existentes.
3. Adicione a nova classe AnaliseCurriculoBI herdando de BaseModel.
4. Regra de Negócio (Validators): Se a IA retornar uma lista para principais_skills ou gaps_identificados, utilize um field_validator (modo before) para converter em string separada por vírgulas, garantindo a estrutura flat.
# Spec para AnaliseCurriculoBI
class AnaliseCurriculoBI(BaseModel):
    nome_candidato: str
    cargo_alvo: str
    score_aderencia: int  # 0 a 100
    nivel_senioridade: str  # Junior, Pleno, Senior, Especialista
    principais_skills: str  # FLAT: "Python, SQL, AWS"
    gaps_identificados: str  # FLAT: "Inglês, Certificação Cloud"
    parecer_resumido: str  # Max 2 frases
🔹 Agente B: Serviço de Persistência (src/services/db_handler.py)
Objetivo: Criar o manipulador de Excel robusto.
1. Crie o arquivo src/services/db_handler.py.
2. Importe pandas as pd, os e openpyxl.
3. Implemente a função salvar_candidato_excel.
4. Lógica Incremental:
    ◦ Verifique os.path.exists(caminho_arquivo).
    ◦ Se existir: df_antigo = pd.read_excel(..., engine='openpyxl').
    ◦ Concatene: df_final = pd.concat([df_antigo, df_novo], ignore_index=True).
    ◦ Se não existir: df_final = df_novo.
5. Tratamento de Erro: Envolva a operação de escrita (to_excel) em um try/except PermissionError.
6. Retorno: (bool, str) -> (True, "Sucesso") ou (False, "Erro: Arquivo aberto").
🔹 Agente C: Integração e Lógica de Negócio (src/services/ai_engine.py & dashboard.py)
Objetivo: Conectar a inteligência existente ao novo formatador e salvar após a análise.
Tarefa C.1: Atualizar src/services/ai_engine.py
1. Importe AnaliseCurriculoBI de src.models.
2. Não substitua o método _executar_gap_analysis, pois o Dashboard usa o retorno dele (AnaliseGap).
3. Crie um método adaptador converter_para_bi(self, dados_gap: dict, nome: str, cargo: str) -> dict.
    ◦ Este método deve mapear os dados do AnaliseGap para o formato AnaliseCurriculoBI.
    ◦ Mapping:
        ▪ score_aderencia <- dados_gap['match_percentual']
        ▪ gaps_identificados <- ", ".join(dados_gap['gaps_tecnicos'])
        ▪ parecer_resumido <- dados_gap['analise_comparativa'][:200]
        ▪ nivel_senioridade <- Inferir baseada no score ou passar como "Não Identificado" se não houver no input.
4. Alternativamente, se for necessária uma nova chamada à LLM para gerar campos específicos (como nivel_senioridade que não existe no AnaliseGap), crie gerar_analise_bi(contexto, vaga) usando o JsonOutputParser(pydantic_object=AnaliseCurriculoBI). Recomendação: Para economizar tokens, tente mapear primeiro.
Tarefa C.2: Atualizar dashboard.py (UI)
1. Importe salvar_candidato_excel de src.services.db_handler.
2. Localize a aba tab1 onde ocorre a chamada res = engine.analisar_documentos(splits, vaga).
3. Logo após a exibição dos resultados (exibir_card_gap ou exibir_card_perfil):
    ◦ Prepare o dicionário de dados para o BI (extraindo o nome do candidato do PDF ou usando "Candidato").
    ◦ Chame salvar_candidato_excel.
    ◦ Exiba o feedback visual:

--------------------------------------------------------------------------------
⚠️ Checklist de Qualidade (DoD)
• [ ] src/models.py compila sem erros de redefinição.
• [ ] O arquivo Excel é criado na primeira execução e anexado nas seguintes.
• [ ] Listas (skills/gaps) aparecem como uma única célula de texto no Excel (sem ['item']).
• [ ] Se o Excel estiver aberto pelo usuário, o Streamlit não trava (exibe erro amigável).
• [ ] Nenhuma funcionalidade visual anterior (gráficos de match, cards) foi removida.