import streamlit as st
import pandas as pd
import sqlite3

from banco import criar_banco

criar_banco()

st.set_page_config(
    page_title="Sistema de Reserva de Salas",
    page_icon="🏫",
    layout="wide"
)
# -------------------------
# CONTROLE DE LOGIN
# -------------------------

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario_nome" not in st.session_state:
    st.session_state.usuario_nome = ""

if "usuario_tipo" not in st.session_state:
    st.session_state.usuario_tipo = ""

if not st.session_state.logado:

    st.title("🔐 Login")

    st.write("Entre com seu e-mail e senha.")

    email_login = st.text_input(
        "E-mail"
    )

    senha_login = st.text_input(
        "Senha",
        type="password"
    )

    if st.button(
        "Entrar",
        width="stretch"
    ):

        conexao = sqlite3.connect("reservas.db")
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT nome, tipo
            FROM usuarios
            WHERE email = ?
            AND senha = ?
            """,
            (
                email_login,
                senha_login
            )
        )

        usuario = cursor.fetchone()

        conexao.close()

        if usuario:

            st.session_state.logado = True
            st.session_state.usuario_nome = usuario[0]
            st.session_state.usuario_tipo = usuario[1]

            st.success("Login realizado com sucesso!")

            st.rerun()

        else:

            st.error(
                "E-mail ou senha inválidos."
            )

    st.stop()

st.title("🏫 Sistema de Reserva de Salas")
st.write("Gerenciamento de salas e solicitações de reservas.")

st.sidebar.write(
    f"👤 **{st.session_state.usuario_nome}**"
)

st.sidebar.write(
    f"Perfil: **{st.session_state.usuario_tipo}**"
)

st.sidebar.divider()

if st.session_state.usuario_tipo == "Administrador":

    pagina = st.sidebar.radio(
        "Menu",
        [
            "Início",
            "Salas",
            "Professores",
            "Reservas",
            "Administração"
        ]
    )

else:

    pagina = st.sidebar.radio(
        "Menu",
        [
            "Início",
            "Reservas"
        ]
    )

st.sidebar.divider()

if st.sidebar.button(
    "🚪 Sair",
    width="stretch"
):

    st.session_state.logado = False
    st.session_state.usuario_nome = ""
    st.session_state.usuario_tipo = ""

    st.rerun()# -------------------------
# CONTROLE DE LOGIN
# -------------------------

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario_nome" not in st.session_state:
    st.session_state.usuario_nome = ""

if "usuario_tipo" not in st.session_state:
    st.session_state.usuario_tipo = ""

if not st.session_state.logado:

    st.title("🔐 Login")

    st.write("Entre com seu e-mail e senha.")

    email_login = st.text_input(
        "E-mail"
    )

    senha_login = st.text_input(
        "Senha",
        type="password"
    )

    if st.button(
        "Entrar",
        width="stretch"
    ):

        conexao = sqlite3.connect("reservas.db")
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT nome, tipo
            FROM usuarios
            WHERE email = ?
            AND senha = ?
            """,
            (
                email_login,
                senha_login
            )
        )

        usuario = cursor.fetchone()

        conexao.close()

        if usuario:

            st.session_state.logado = True
            st.session_state.usuario_nome = usuario[0]
            st.session_state.usuario_tipo = usuario[1]

            st.success("Login realizado com sucesso!")

            st.rerun()

        else:

            st.error(
                "E-mail ou senha inválidos."
            )

    st.stop()

st.title("🏫 Sistema de Reserva de Salas")
st.write("Gerenciamento de salas e solicitações de reservas.")

st.sidebar.write(
    f"👤 **{st.session_state.usuario_nome}**"
)

st.sidebar.write(
    f"Perfil: **{st.session_state.usuario_tipo}**"
)

st.sidebar.divider()

if st.session_state.usuario_tipo == "Administrador":

    pagina = st.sidebar.radio(
        "Menu",
        [
            "Início",
            "Salas",
            "Professores",
            "Reservas",
            "Administração"
        ]
    )

else:

    pagina = st.sidebar.radio(
        "Menu",
        [
            "Início",
            "Reservas"
        ]
    )

st.sidebar.divider()

if st.sidebar.button(
    "🚪 Sair",
    width="stretch"
):

    st.session_state.logado = False
    st.session_state.usuario_nome = ""
    st.session_state.usuario_tipo = ""

    st.rerun()