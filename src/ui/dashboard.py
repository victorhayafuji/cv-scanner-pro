import streamlit as st
import time
from src.config import Config
from src.services.pdf_handler import processar_pdf
from src.services.ai_engine import AIEngine


@st.cache_resource
def carregar_motor_ia():
    return AIEngine()


def injetar_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        .st-emotion-cache-1r6slb0, .st-emotion-cache-12w0pgk { border-radius: 12px; border: 1px solid #3a3a3a; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .stButton>button { border-radius: 20px; height: 3em; font-weight: 600; }
        [data-testid="stMetricValue"] { font-size: 2.5rem; font-weight: 700; }
        /* Destaque para placeholders */
        .placeholder-metric { color: #ffbd45; font-weight: bold; background: #3d3024; padding: 2px 6px; border-radius: 4px; }
        </style>
    """, unsafe_allow_html=True)


def render_tag(texto, tipo="neutro"):
    cores = {
        "neutro": ("#262730", "#4e4e4e"),
        "sucesso": ("#1e3a29", "#2e5c40"),
        "erro": ("#3a1e1e", "#5c2e2e")
    }
    bg, border = cores.get(tipo, cores["neutro"])
    return f"""<span style="background-color:{bg}; color:#fff; border:1px solid {border}; padding:4px 10px; border-radius:15px; font-size:0.8em; margin:3px; display:inline-block; font-weight:500;">{texto}</span>"""


# --- TELAS DE ANÁLISE (Mantidas iguais) ---
def exibir_landing_page():
    st.markdown("---")
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("## 🚀 Turbine seu CV com IA")
        st.write("Receba uma análise de CTO e **reescreva seu currículo** automaticamente.")
    with c2: st.info("👈 **Comece:** Upload do PDF na barra lateral.", icon="📂")


def exibir_card_perfil(dados):
    # (Código visual do Perfil que já fizemos...)
    with st.container(border=True):
        c1, c2, c3 = st.columns([1, 4, 2])
        with c1:
            nome_url = dados.get("nome", "User").replace(" ", "+")
            st.image(f"https://ui-avatars.com/api/?name={nome_url}&background=0D8ABC&color=fff&size=128&bold=true",
                     width=100)
        with c2:
            st.title(dados.get("nome"))
            st.markdown(f"**{dados.get('cargo_atual')}**")
            st.caption(f"⏱️ {dados.get('tempo_experiencia')}")
            st.markdown(
                "Stack Principal: " + "".join([render_tag(s) for s in dados.get("skills_tecnicas", [])[:6]]) + "...",
                unsafe_allow_html=True)
        with c3:
            score = dados.get("score_geral", 0)
            st.metric("Score", f"{score}/100", delta="Mercado", delta_color="normal")

    st.markdown("### 🧐 Veredito")
    st.info(dados.get("justificativa_score"), icon="🤖")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🚀 Pontos Fortes")
        for p in dados.get("pontos_fortes", []): st.markdown(f"✅ {p}")
    with c2:
        st.markdown("### ⚠️ Atenção")
        for p in dados.get("pontos_atencao", []): st.markdown(f"🔻 {p}")


def exibir_card_gap(dados):
    # (Código visual do Gap Analysis que já fizemos...)
    match = dados.get("match_percentual", 0)
    st.markdown(f"### 🎯 Aderência: {match}%")
    st.progress(min(max(match, 0), 100) / 100)
    st.write(dados.get("analise_comparativa"))
    c1, c2 = st.columns(2)
    with c1:
        st.success("✅ O que você TEM")
        st.markdown("".join([render_tag(s, "sucesso") for s in dados.get("pontos_fortes", [])]), unsafe_allow_html=True)
    with c2:
        st.error("❌ O que FALTA")
        st.markdown("".join([render_tag(s, "erro") for s in dados.get("gaps_tecnicos", [])]), unsafe_allow_html=True)

# --- ATUALIZAÇÃO NESTA FUNÇÃO: ---
def exibir_otimizador(engine, splits, vaga=None):
    st.markdown("### ✨ Otimizador de Conteúdo (AI Writer)")
    st.write("Abaixo, uma versão reescrita do seu perfil focada em **Impacto** e **Senioridade**.")

    if st.button("⚡ Gerar Versão Otimizada", type="primary"):
        with st.spinner("Reescrevendo e auditando veracidade..."):
            otimizado = engine.otimizar_cv(splits, vaga)

            # 1. Resumo
            with st.container(border=True):
                st.subheader("📝 Novo Resumo Profissional")
                st.code(otimizado.get("resumo_profissional_novo"), language="text")
                st.caption("Copie este texto para o topo do seu CV/LinkedIn.")

            # 2. Experiências (Bullets)
            with st.container(border=True):
                st.subheader("💼 Experiências Turbinadas (Método STAR)")
                st.write("Substitua seus bullet points antigos por estes:")

                for bullet in otimizado.get("bullets_experiencia_star", []):
                    # Highlight visual nos placeholders [X]
                    bullet_formatado = bullet.replace("[", "<span class='placeholder-metric'>[").replace("]",
                                                                                                         "]</span>")
                    st.markdown(f"🔸 {bullet_formatado}", unsafe_allow_html=True)

                st.info("💡 **Dica:** Onde estiver amarelo, insira seus números reais (ex: 20%, R$ 50k, 3 dias).")

            # --- NOVO: BLOCO REALITY CHECK ---
            st.markdown("---")
            with st.container(border=True):
                st.markdown("### 🕵️ Reality Check (Auditoria de Veracidade)")
                st.markdown(
                    "_A IA foi agressiva na venda. Verifique estes pontos para não cair em contradição na entrevista:_")

                for alerta in otimizado.get("reality_check", []):
                    # Ícone de alerta piscando mentalmente
                    st.error(f"⚠️ {alerta}", icon="🚨")

            # 3. Log de Melhorias (agora no fim)
            with st.expander("Ver log técnico de melhorias"):
                for m in otimizado.get("melhorias_realizadas", []):
                    st.markdown(f"- {m}")


# --- MAIN ---
def renderizar_interface():
    st.set_page_config(page_title="CV Engine Pro", page_icon="🧩", layout="wide")
    injetar_css()
    st.title("🧩 CV Engine Pro v3.0 (Final)")

    if "motor_carregado" not in st.session_state:
        try:
            Config.validar()
            carregar_motor_ia()
            st.session_state["motor_carregado"] = True
        except Exception as e:
            st.error(f"Erro config: {e}")
            st.stop()

    with st.sidebar:
        st.header("📂 Upload")
        arquivo = st.file_uploader("Seu Currículo (PDF)", type="pdf")
        st.divider()
        st.header("🎯 Vaga Alvo")
        vaga = st.text_area("Descrição da Vaga...", height=200)

    if arquivo:
        # SISTEMA DE ABAS
        tab1, tab2 = st.tabs(["📊 Análise & Diagnóstico", "✨ Otimizador de Texto"])

        # Variável para guardar splits e evitar reprocessar
        if "splits" not in st.session_state:
            st.session_state["splits"] = processar_pdf(arquivo)

        splits = st.session_state["splits"]
        engine = carregar_motor_ia()

        with tab1:
            if st.button("🔍 Rodar Análise", type="primary", key="btn_analise"):
                with st.spinner("Analisando..."):
                    try:
                        res = engine.analisar_documentos(splits, vaga)
                        if vaga:
                            exibir_card_gap(res)
                        else:
                            exibir_card_perfil(res)
                        
                        # --- NOVO: SALVAR NO BI ---
                        try:
                            from src.services.db_handler import salvar_candidato_excel
                            
                            # --- CORREÇÃO: Extração Inteligente do Nome ---
                            nome_limpo_arquivo = arquivo.name.replace(".pdf", "").replace("_", " ").title()
                            nome_candidato = res.get("nome", nome_limpo_arquivo)
                            
                            if vaga:
                                dados_bi = engine.converter_para_bi(res, nome_candidato, vaga)
                                sucesso, msg = salvar_candidato_excel(dados_bi)
                                if sucesso:
                                    st.toast(f"✅ {msg}", icon="💾")
                                else:
                                    st.warning(f"⚠️ BI: {msg}")
                        except Exception as e:
                            st.error(f"Erro ao salvar no BI: {e}")

                    except Exception as e:
                        st.error(f"Erro na Análise: {str(e)}")
                        # Opcional: mostrar stack trace
                        # import traceback
                        # st.code(traceback.format_exc())

        with tab2:
            exibir_otimizador(engine, splits, vaga)

    else:
        exibir_landing_page()


if __name__ == "__main__":
    renderizar_interface()