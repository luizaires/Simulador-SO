import streamlit as st
from utils.session import inicializar_sessao
import plotly.express as px
import pandas as pd

inicializar_sessao()

st.title("Gerenciar Memória")

st.write("""
Nesta área será exibida a ocupação da memória pelos processos.
""")

with st.sidebar:

    st.subheader("Configuração da Memória")

    st.session_state.memoria_total = st.number_input(
        "Frames Totais",
        min_value=10,
        value=st.session_state.memoria_total,
        step=1
    )

memoria_total = st.session_state.memoria_total

frames_ocupados = sum(
    processo["Frames"]
    for processo in st.session_state.processos
)

if frames_ocupados > memoria_total:
    st.error(
        "A memória está superalocada. Existem mais frames utilizados do que disponíveis."
    )
else:
    frames_livres = memoria_total - frames_ocupados

    uso_memoria = (
        frames_ocupados / memoria_total
    ) * 100

    st.subheader("Uso de Memória-Métricas")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Frames Totais",
            memoria_total
        )

    with col2:
        st.metric(
        "Frames Ocupados",
        frames_ocupados
    )

    with col3:
        st.metric(
        "Frames Livres",
        frames_livres
    )

    st.subheader("Taxa de Ocupação da Memória")
    
    st.progress(uso_memoria / 100)

    st.write(f"{uso_memoria:.1f}% utilizada")


st.subheader("Alocação de Frames por Processo")

dados = []

for processo in st.session_state.processos:
    dados.append({
        "Processo": processo["Nome"],
        "Frames": processo["Frames"]
    })

if frames_livres > 0:

    dados.append({
        "Processo": "Livre",
        "Frames": frames_livres
    })

if dados:

    df = pd.DataFrame(dados)

    fig = px.treemap(
        df,
        path=["Processo"],
        values="Frames"
    )

    fig.update_traces(
        hovertemplate=
        "<b>%{label}</b><br>" +
        "Frames: %{value}<br>" +
        "Uso: %{percentRoot:.1%}<extra></extra>"
    )

    st.plotly_chart(fig)


else:

    st.info("Nenhum processo ocupando memória.")
