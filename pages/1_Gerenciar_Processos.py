import streamlit as st
import pandas as pd
from utils.session import inicializar_sessao
import plotly.express as px
import plotly.graph_objects as go

inicializar_sessao()


st.title("Gerenciar Processos")

st.write("""
Nesta área serão cadastrados e monitorados os processos
da simulação.
""")


with st.sidebar:

    st.subheader("Cadastrar Processo")


    nome = st.text_input(
        "Nome do Processo"
    )

    tempo_execucao = st.number_input(
        "Tempo de Execução",
        min_value=1,
        value=1
    )

    frames = st.number_input(
        "Quantidade de Frames",
        min_value=1,
        value=1
    )
    
    frames_ocupados = sum(
    processo["Frames"]
    for processo in st.session_state.processos
)

    if st.button("Adicionar Processo"):

        processo = {
            "PID": st.session_state.proximo_pid,
            "Nome": nome,
            "Tempo Execução": tempo_execucao,
            "Tempo Restante": tempo_execucao,
            "Frames": frames,
            "Estado": "PRONTO"
        }

        if frames_ocupados + processo["Frames"] > st.session_state.memoria_total:

            st.error(
                "Memória insuficiente para alocar o processo."
            )

        else:

            st.session_state.processos.append(processo)

            st.session_state.proximo_pid += 1

            st.success("Processo criado com sucesso!")

            st.rerun()  
    
    if st.button(
        "Limpar Processos",
        width="stretch"
    ):

        st.session_state.processos = []
        st.session_state.proximo_pid = 1

        st.rerun()

st.subheader("Tabela de Processos")



def calcular_tempo_medio_execucao(processos):

    if not processos:
        return 0

    return sum(
        p["Tempo Execução"]
        for p in processos
    ) / len(processos)

tempo_medio_execucao = calcular_tempo_medio_execucao(
    st.session_state.processos
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Quantidade de Processos",
        len(st.session_state.processos)
    )

with col2:
    st.metric(
        "Tempo Médio de Execução",
        f"{tempo_medio_execucao:.1f}"
    )
    
if st.session_state.processos:

    df = pd.DataFrame(st.session_state.processos)

    st.data_editor(
    df,
    width="stretch",
    hide_index=True,
    disabled=True
)

else:

    st.info("Nenhum processo cadastrado.")

if st.session_state.processos:
    fila_sjf = sorted(
        st.session_state.processos,
        key=lambda p: p["Tempo Execução"]
    )

    tempo_atual = 0

    gantt = []

    for processo in fila_sjf:

        inicio = tempo_atual

        fim = inicio + processo["Tempo Execução"]

        gantt.append({
            "Processo": processo["Nome"],
            "Inicio": inicio,
            "Fim": fim
        })

        tempo_atual = fim


    fig = go.Figure()

    for processo in gantt:

        fig.add_trace(
            go.Bar(
                y=[processo["Processo"]],
                x=[processo["Fim"] - processo["Inicio"]],
                base=processo["Inicio"],
                orientation="h",
                name=processo["Processo"]
            )
        )

    fig.update_layout(
        title="Escalonamento SJF",
        xaxis_title="Tempo",
        yaxis_title="Processos",
        barmode="stack"
    )

    st.plotly_chart(fig)

    if "fila_prontos" not in st.session_state:
        st.session_state.fila_prontos = []

    if "processo_executando" not in st.session_state:
        st.session_state.processo_executando = None

    if "processos_finalizados" not in st.session_state:
        st.session_state.processos_finalizados = []

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Prontos")

    with col2:
        st.subheader("Executando")

    with col3:
        st.subheader("Finalizados")

    if fila_sjf:

        st.session_state.processo_executando = fila_sjf[0]

        st.session_state.processo_executando["Estado"] = "EXECUTANDO"

    if st.button("Run"):
        st.session_state.processo_executando["Tempo Restante"] -= 1

    if (st.session_state.processo_executando["Tempo Restante"] == 0):
        st.session_state.processo_executando["Estado"] = "FINALIZADO"

    st.session_state.processos_finalizados.append(
        st.session_state.processo_executando
    )

    proximos = sorted([p for p in st.session_state.processos if p["Estado"] == "PRONTO"],
        key=lambda p: p["Tempo Execução"]
    )

    if proximos:

        st.session_state.processo_executando = proximos[0]

        st.session_state.processo_executando["Estado"] = "EXECUTANDO"