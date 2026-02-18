# 🧩 CV Engine Pro

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688?style=flat&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-14%2B-black?style=flat&logo=next.js)
![LangChain](https://img.shields.io/badge/AI-LangChain-green?style=flat)
![License](https://img.shields.io/badge/License-Proprietary-red?style=flat)

**Plataforma SaaS B2B de Triagem Inteligente de Candidatos (AI Screening) para times de Recursos Humanos.**

O **CV Engine Pro** automatiza a análise de currículos em larga escala utilizando inteligência artificial (RAG). O sistema cruza perfis de candidatos (PDFs) com descrições de vagas (Job Descriptions), gerando scores matemáticos de aderência, identificando gaps técnicos e fornecendo um dashboard analítico nativo para a tomada de decisão executiva.

---

## 🏗️ Arquitetura da Solução

O projeto segue uma arquitetura desacoplada (Client-Server), focada em performance e governança de dados:

* **Front-end (Dashboard Interativo):** Desenvolvido em Next.js com Tailwind CSS (paleta *Corporate Blue*). Utiliza Recharts para visualização de dados em padrão *Bento Grid*.
* **Back-end (API Gateway):** Construído em Python (FastAPI), expondo endpoints RESTful assíncronos e protegidos.
* **Motor Cognitivo (AI Core):** Orquestrado via LangChain consumindo o modelo Google Gemini 2.5 Flash para extração de entidades sem alucinação.
* **Segurança:** Autenticação via JWT (OAuth2) com senhas cacheadas (bcrypt).
* **Camada de Persistência (MVP):** Utiliza a biblioteca `pandas` para gerenciar arquivos estruturados (`usuarios.xlsx` para controle de acesso e `dados_bi.xlsx` como Data Warehouse analítico).

---

## 🚀 Funcionalidades Principais

* **Ingestão em Lote (Batch Processing):** Upload simultâneo de múltiplos PDFs de currículos.
* **Score de Aderência:** Motor de IA que calcula o *match* (0-100) do candidato contra os requisitos técnicos da vaga.
* **Gap Analysis:** Extração estruturada de tecnologias e competências que faltam no perfil avaliado.
* **Dashboard Executivo Nativo:** Acompanhamento em tempo real de KPIs de recrutamento (Taxa de Aprovação, Volume de Candidatos, Distribuição de Senioridade).
* **Exportação de Dados:** Arquitetura pronta para plugar o Excel gerado diretamente no Power BI, se necessário.

---

## ⚙️ Pré-requisitos

* **Python 3.10+**
* **Node.js 18+** (LTS)
* **Chave de API:** Google AI Studio (Gemini)

---

## 🛠️ Instalação e Execução (Quick Start)

### 🚀 Modo Automático (Recomendado)

O projeto possui um orquestrador inteligente que sobe **Backend** e **Frontend** simultaneamente, gerenciando portas e ambientes virtuais.

1. Ative seu ambiente virtual (se ainda não estiver ativo):
   ```bash
   # Windows
   venv\Scripts\activate
   ```

2. Execute o launcher principal:
   ```bash
   python main.py
   ```
   *Isso iniciará a API na porta 8000 e o Frontend na porta 5173.*

---

### 🛡️ Testes de Segurança (Security)

O projeto inclui um script automatizado de verificação de segurança (`security_tests.py`) que testa:
* ✅ **Auth Bypass:** Tentativa de acesso a rotas protegidas sem token.
* ✅ **SQL Injection:** Tentativa de injeção de SQL no login.
* ✅ **XSS (Cross-Site Scripting):** Tratamento de payloads maliciosos.
* ✅ **Rate Limiting:** Verificação de resistência a flood de requisições.
* ✅ **Upload Malicioso:** Bloqueio de arquivos executáveis (.exe, .py).

Para rodar a bateria de testes (o script sobe e desce o servidor automaticamente):
```bash
python security_tests.py
```

---

### ⚙️ Execução Manual (Modo Avançado)

Caso prefira rodar os serviços separadamente em terminais distintos:

#### 1. Back-end (FastAPI)
```bash
# Certifique-se de estar no venv
uvicorn src.api:app --reload --port 8000
```

#### 2. Front-end (Next.js/Vite)
```bash
cd frontend
npm run dev
```
*O SaaS estará disponível em: `http://localhost:5173`*

---

## 📊 Dicionário de Dados (Data Dictionary)

O sistema centraliza a inteligência gerada no artefato `dados_bi.xlsx`. As colunas garantem a integridade do Dashboard:

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `nome_candidato` | String | Nome completo extraído pela IA. |
| `cargo_alvo` | String | Título da vaga utilizada para o cruzamento. |
| `score_aderencia` | Integer | Nota final (0-100) validada. Define a classificação (Elite, Qualificado, etc). |
| `nivel_senioridade` | String | Classificação de mercado inferida (ex: Júnior, Pleno, Sênior). |
| `principais_skills` | String | Tecnologias e competências mapeadas no currículo. |
| `gaps_identificados` | String | Requisitos obrigatórios da vaga não encontrados no perfil. |
| `parecer_resumido` | String | Justificativa técnica gerada pela IA para o score atribuído. |
| `data_analise` | Datetime | Timestamp da triagem para análise de séries temporais. |
