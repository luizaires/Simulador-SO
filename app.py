import streamlit as st

st.set_page_config(
    page_title="Simulador de Sistema Operacional",
    page_icon="💻",
    layout="wide"
)

st.title("💻 Simulador de Sistema Operacional")

st.write(
    """
    Projeto da discplina de Sistemas Operacionas, consistindo de um simulador que realiza o gerenciamento
    de processos utilizando o algoritmo de escalonamento SJF (Shortest Job First).

    Funcionalidades:
    - Cadastro de processos
    - Escalonamento SJF
    - Gerenciamento de memória
    - Visualização dos estados dos processos
    """
)

st.info("Utilize o menu lateral para navegar pelas funcionalidades do sistema.")