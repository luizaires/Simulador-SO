import streamlit as st

def inicializar_sessao():

    if "processos" not in st.session_state:
        st.session_state.processos = []

    if "proximo_pid" not in st.session_state:
        st.session_state.proximo_pid = 1

    if "memoria_total" not in st.session_state:
        st.session_state.memoria_total = 10