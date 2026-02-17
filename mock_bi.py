import pandas as pd
import random
from datetime import datetime, timedelta

def gerar_mock_contextual(caminho_base="dados_bi.xlsx - Sheet1.csv", quantidade=200, saida="dados_bi_mock.xlsx"):
    try:
        df_base = pd.read_csv(caminho_base, sep=None, engine='python')
        colunas = df_base.columns.tolist()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_base}' não foi encontrado.")
        return

    primeiros_nomes = ["Ana", "Carlos", "Fernanda", "João", "Mariana", "Victor", "Lucas", "Beatriz", "Pedro", "Camila", "Rodrigo", "Juliana", "Rafael", "Amanda", "Bruno"]
    sobrenomes = ["Silva", "Souza", "Lima", "Costa", "Aguiar", "Rocha", "Mendes", "Santos", "Oliveira", "Pereira", "Ferreira", "Alves", "Ribeiro", "Gomes", "Martins"]
    vagas = ["Analista de BI Pleno", "Engenheiro de Dados", "Cientista de Dados", "Analista de Dados Senior"]
    
    # 1. Pré-geração de Nomes Únicos
    nomes_gerados = set()
    while len(nomes_gerados) < quantidade:
        s1, s2 = random.sample(sobrenomes, 2) 
        nome = f"{random.choice(primeiros_nomes)} {s1} {s2}"
        nomes_gerados.add(nome)

    lista_nomes_unicos = list(nomes_gerados)
    
    dados = []
    
    # 2. Definição da Janela de Tempo (01/01/2025 até o instante atual)
    hoje = datetime.now()
    data_inicio = datetime(2025, 1, 1)
    segundos_totais = int((hoje - data_inicio).total_seconds())

    for i in range(quantidade):
        score = random.randint(10, 100)
        
        # Lógica Contextual (Senioridade vs Score)
        if score >= 80:
            nivel = "Senior/Especialista"
            parecer = "Candidato apresenta excelente alinhamento com a vaga. Domínio técnico comprovado e forte bagagem."
            gaps = "Não há gaps técnicos diretos nos requisitos explícitos da vaga."
            skills = "Domínio avançado das ferramentas principais (SQL, Power BI/Python). Excelente capacidade analítica."
        elif score >= 50:
            nivel = "Pleno"
            parecer = "Candidato possui boa base técnica, mas carece de experiência em projetos de maior escala."
            gaps = "Falta aprofundamento em arquitetura de dados e modelagem dimensional avançada."
            skills = "Conhecimento intermediário nas ferramentas principais. Boa capacidade de execução sob supervisão."
        else:
            nivel = "Júnior/Estágio"
            parecer = "Perfil ainda em desenvolvimento. O candidato não atende aos requisitos mínimos de experiência."
            gaps = "Ausência de conhecimento prático nas tecnologias exigidas. Necessita de forte capacitação."
            skills = "Conceitos teóricos básicos. Familiaridade inicial e acadêmica com as ferramentas."

        linha = {}
        for col in colunas:
            col_lower = col.lower()
            if "data" in col_lower:
                # Sorteia um segundo aleatório dentro da janela de tempo e soma à data de início
                segundos_aleatorios = random.randint(0, segundos_totais)
                data_aleatoria = data_inicio + timedelta(seconds=segundos_aleatorios)
                linha[col] = data_aleatoria.strftime("%Y-%m-%d %H:%M:%S")
            elif "nome" in col_lower or "candidato" in col_lower:
                linha[col] = lista_nomes_unicos[i]
            elif "cargo" in col_lower or "vaga" in col_lower:
                linha[col] = random.choice(vagas)
            elif "score" in col_lower or "aderencia" in col_lower:
                linha[col] = score
            elif "senioridade" in col_lower:
                linha[col] = nivel
            elif "gaps" in col_lower:
                linha[col] = gaps
            elif "parecer" in col_lower:
                linha[col] = parecer
            elif "skills" in col_lower or "fortes" in col_lower:
                linha[col] = skills
            else:
                linha[col] = "Dado gerado"
                
        dados.append(linha)

    df_mock = pd.DataFrame(dados)
    
    # Ordenação cronológica (do mais recente para o mais antigo)
    colunas_data = [c for c in colunas if "data" in c.lower()]
    if colunas_data:
        df_mock = df_mock.sort_values(by=colunas_data[0], ascending=False)

    df_mock.to_excel(saida, index=False, engine='openpyxl')
    print(f"✅ Arquivo '{saida}' gerado! {quantidade} currículos com datas distribuídas entre 2025 e Hoje.")

if __name__ == "__main__":
    gerar_mock_contextual()