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
    
# -------------------------
# INÍCIO
# -------------------------

if pagina == "Início":

    st.header("📊 Painel Principal")

    conexao = sqlite3.connect("reservas.db")
    cursor = conexao.cursor()

    if st.session_state.usuario_tipo == "Professor":

        nome_professor = st.session_state.usuario_nome

        cursor.execute(
            """
            SELECT id
            FROM professores
            WHERE nome = ?
            """,
            (nome_professor,)
        )

        resultado = cursor.fetchone()

        if resultado:
            professor_id = resultado[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM reservas
                WHERE professor_id = ?
                """,
                (professor_id,)
            )
            total_minhas = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM reservas
                WHERE professor_id = ?
                AND status = 'Pendente'
                """,
                (professor_id,)
            )
            total_pendentes = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM reservas
                WHERE professor_id = ?
                AND status = 'Aprovada'
                """,
                (professor_id,)
            )
            total_aprovadas = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM reservas
                WHERE professor_id = ?
                AND status = 'Cancelada'
                """,
                (professor_id,)
            )
            total_canceladas = cursor.fetchone()[0]

        else:
            total_minhas = 0
            total_pendentes = 0
            total_aprovadas = 0
            total_canceladas = 0

        conexao.close()

        st.subheader(
            f"👨‍🏫 Bem-vindo, {st.session_state.usuario_nome}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📅 Minhas Reservas",
                total_minhas
            )

        with col2:
            st.metric(
                "⏳ Pendentes",
                total_pendentes
            )

        with col3:
            st.metric(
                "✅ Aprovadas",
                total_aprovadas
            )

        with col4:
            st.metric(
                "🚫 Canceladas",
                total_canceladas
            )

        st.divider()

        st.info(
            "Use o menu lateral para realizar novas reservas "
            "e acompanhar o status das suas solicitações."
        )

    else:

        cursor.execute(
            "SELECT COUNT(*) FROM salas"
        )
        total_salas = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM professores"
        )
        total_professores = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM reservas
            WHERE status = 'Pendente'
            """
        )
        total_pendentes = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM reservas
            WHERE status = 'Aprovada'
            """
        )
        total_aprovadas = cursor.fetchone()[0]

        conexao.close()

        st.subheader("⚙️ Visão do Administrador")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🏫 Salas",
                total_salas
            )

        with col2:
            st.metric(
                "👨‍🏫 Professores",
                total_professores
            )

        with col3:
            st.metric(
                "⏳ Pendentes",
                total_pendentes
            )

        with col4:
            st.metric(
                "✅ Aprovadas",
                total_aprovadas
            )

        st.divider()

        st.info(
            "Use o menu lateral para cadastrar salas, "
            "professores, gerenciar reservas e analisar solicitações."
        )
