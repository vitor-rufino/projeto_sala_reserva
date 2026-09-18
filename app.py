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

# -------------------------
# SALAS
# -------------------------

elif pagina == "Salas":

    st.header("🏫 Cadastro de Salas")

    # CADASTRAR SALA
    with st.form("form_sala"):

        nome = st.text_input("Nome da sala")

        capacidade = st.number_input(
            "Capacidade",
            min_value=1,
            step=1
        )

        localizacao = st.text_input("Localização")

        projetor = st.selectbox(
            "Possui projetor?",
            ["Sim", "Não"]
        )

        computadores = st.number_input(
            "Quantidade de computadores",
            min_value=0,
            step=1
        )

        cadastrar = st.form_submit_button(
            "Cadastrar Sala"
        )

        if cadastrar:

            if nome.strip() == "" or localizacao.strip() == "":

                st.warning(
                    "Preencha todos os campos obrigatórios."
                )

            else:

                conexao = sqlite3.connect("reservas.db")
                cursor = conexao.cursor()

                cursor.execute(
                    """
                    INSERT INTO salas
                    (
                        nome,
                        capacidade,
                        localizacao,
                        projetor,
                        computadores,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        nome,
                        capacidade,
                        localizacao,
                        projetor,
                        computadores,
                        "Disponível"
                    )
                )

                conexao.commit()
                conexao.close()

                st.success(
                    "Sala cadastrada com sucesso!"
                )

                st.rerun()

    # LISTAR SALAS
    st.divider()

    st.subheader("📋 Salas cadastradas")

    conexao = sqlite3.connect("reservas.db")

    salas = pd.read_sql_query(
        "SELECT * FROM salas ORDER BY nome",
        conexao
    )

    conexao.close()

    if salas.empty:

        st.info("Nenhuma sala cadastrada.")

    else:

        st.dataframe(
            salas,
            width="stretch"
        )

        # EDITAR OU EXCLUIR
        st.divider()

        st.subheader("✏️ Editar ou Excluir Sala")

        sala_selecionada = st.selectbox(
            "Selecione uma sala",
            salas["nome"].tolist(),
            key="editar_sala"
        )

        dados_sala = salas[
            salas["nome"] == sala_selecionada
        ].iloc[0]

        novo_nome = st.text_input(
            "Novo nome",
            value=str(dados_sala["nome"])
        )

        nova_capacidade = st.number_input(
            "Nova capacidade",
            min_value=1,
            value=int(dados_sala["capacidade"]),
            step=1
        )

        nova_localizacao = st.text_input(
            "Nova localização",
            value=str(dados_sala["localizacao"])
        )

        novo_projetor = st.selectbox(
            "Possui projetor?",
            ["Sim", "Não"],
            index=0
            if dados_sala["projetor"] == "Sim"
            else 1,
            key="novo_projetor"
        )

        novos_computadores = st.number_input(
            "Quantidade de computadores",
            min_value=0,
            value=int(dados_sala["computadores"]),
            step=1
        )

        col_editar, col_excluir = st.columns(2)

        # SALVAR ALTERAÇÃO
        with col_editar:

            if st.button(
                "💾 Salvar Alterações",
                use_container_width=True
            ):

                if novo_nome.strip() == "" or nova_localizacao.strip() == "":

                    st.warning(
                        "Nome e localização não podem ficar vazios."
                    )

                else:

                    conexao = sqlite3.connect("reservas.db")
                    cursor = conexao.cursor()

                    cursor.execute(
                        """
                        UPDATE salas
                        SET
                            nome = ?,
                            capacidade = ?,
                            localizacao = ?,
                            projetor = ?,
                            computadores = ?
                        WHERE id = ?
                        """,
                        (
                            novo_nome,
                            nova_capacidade,
                            nova_localizacao,
                            novo_projetor,
                            novos_computadores,
                            int(dados_sala["id"])
                        )
                    )

                    conexao.commit()
                    conexao.close()

                    st.success(
                        "Sala atualizada com sucesso!"
                    )

                    st.rerun()

        # EXCLUIR SALA
        with col_excluir:

            if st.button(
                "🗑️ Excluir Sala",
                use_container_width=True
            ):

                conexao = sqlite3.connect("reservas.db")
                cursor = conexao.cursor()

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM reservas
                    WHERE sala_id = ?
                    """,
                    (int(dados_sala["id"]),)
                )

                total_reservas = cursor.fetchone()[0]

                if total_reservas > 0:

                    st.error(
                        "Não é possível excluir esta sala "
                        "porque ela possui reservas vinculadas."
                    )

                    conexao.close()

                else:

                    cursor.execute(
                        """
                        DELETE FROM salas
                        WHERE id = ?
                        """,
                        (int(dados_sala["id"]),)
                    )

                    conexao.commit()
                    conexao.close()

                    st.success(
                        "Sala excluída com sucesso!"
                    )

                    st.rerun()

# -------------------------
# PROFESSORES
# -------------------------

elif pagina == "Professores":

    st.header("👨‍🏫 Cadastro de Professores")

    # CADASTRAR PROFESSOR
    with st.form("form_professor"):

        nome = st.text_input("Nome do professor")
        email = st.text_input("E-mail")
        departamento = st.text_input("Departamento / Curso")

        cadastrar_professor = st.form_submit_button(
            "Cadastrar Professor"
        )

        if cadastrar_professor:

            if (
                nome.strip() == ""
                or email.strip() == ""
                or departamento.strip() == ""
            ):

                st.warning("Preencha todos os campos.")

            else:

                conexao = sqlite3.connect("reservas.db")
                cursor = conexao.cursor()

                try:

                    cursor.execute(
                        """
                        INSERT INTO professores
                        (nome, email, departamento)
                        VALUES (?, ?, ?)
                        """,
                        (
                            nome,
                            email,
                            departamento
                        )
                    )

                    conexao.commit()

                    st.success(
                        "Professor cadastrado com sucesso!"
                    )

                    st.rerun()

                except sqlite3.IntegrityError:

                    st.error(
                        "Já existe um professor cadastrado "
                        "com esse e-mail."
                    )

                finally:

                    conexao.close()

    # LISTAR PROFESSORES
    st.divider()

    st.subheader("📋 Professores cadastrados")

    conexao = sqlite3.connect("reservas.db")

    professores = pd.read_sql_query(
        "SELECT * FROM professores ORDER BY nome",
        conexao
    )

    conexao.close()

    if professores.empty:

        st.info("Nenhum professor cadastrado.")

    else:

        st.dataframe(
            professores,
            width="stretch"
        )

        # EDITAR OU EXCLUIR
        st.divider()

        st.subheader("✏️ Editar ou Excluir Professor")

        professor_selecionado = st.selectbox(
            "Selecione um professor",
            professores["nome"].tolist(),
            key="editar_professor"
        )

        dados_professor = professores[
            professores["nome"] == professor_selecionado
        ].iloc[0]

        novo_nome_professor = st.text_input(
            "Nome",
            value=str(dados_professor["nome"]),
            key="novo_nome_professor"
        )

        novo_email = st.text_input(
            "E-mail",
            value=str(dados_professor["email"]),
            key="novo_email_professor"
        )

        novo_departamento = st.text_input(
            "Departamento / Curso",
            value=str(dados_professor["departamento"]),
            key="novo_departamento_professor"
        )

        col_editar_prof, col_excluir_prof = st.columns(2)

        # SALVAR ALTERAÇÕES
        with col_editar_prof:

            if st.button(
                "💾 Salvar Alterações",
                key="salvar_professor",
                use_container_width=True
            ):

                if (
                    novo_nome_professor.strip() == ""
                    or novo_email.strip() == ""
                    or novo_departamento.strip() == ""
                ):

                    st.warning(
                        "Nenhum campo pode ficar vazio."
                    )

                else:

                    conexao = sqlite3.connect("reservas.db")
                    cursor = conexao.cursor()

                    try:

                        cursor.execute(
                            """
                            UPDATE professores

                            SET nome = ?,
                                email = ?,
                                departamento = ?

                            WHERE id = ?
                            """,
                            (
                                novo_nome_professor,
                                novo_email,
                                novo_departamento,
                                int(dados_professor["id"])
                            )
                        )

                        conexao.commit()

                        st.success(
                            "Professor atualizado com sucesso!"
                        )

                        st.rerun()

                    except sqlite3.IntegrityError:

                        st.error(
                            "Este e-mail já está sendo "
                            "utilizado por outro professor."
                        )

                    finally:

                        conexao.close()

        # EXCLUIR PROFESSOR
        with col_excluir_prof:

            if st.button(
                "🗑️ Excluir Professor",
                key="excluir_professor",
                use_container_width=True
            ):

                conexao = sqlite3.connect("reservas.db")
                cursor = conexao.cursor()

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM reservas
                    WHERE professor_id = ?
                    """,
                    (int(dados_professor["id"]),)
                )

                total_reservas = cursor.fetchone()[0]

                if total_reservas > 0:

                    st.error(
                        "Não é possível excluir este professor "
                        "porque existem reservas vinculadas a ele."
                    )

                    conexao.close()

                else:

                    cursor.execute(
                        """
                        DELETE FROM professores
                        WHERE id = ?
                        """,
                        (int(dados_professor["id"]),)
                    )

                    conexao.commit()
                    conexao.close()

                    st.success(
                        "Professor excluído com sucesso!"
                    )

                    st.rerun()
# -------------------------
# RESERVAS
# -------------------------

elif pagina == "Reservas":

    st.header("📅 Solicitação de Reserva")

    conexao = sqlite3.connect("reservas.db")

    professores = pd.read_sql_query(
        "SELECT * FROM professores ORDER BY nome",
        conexao
    )

    salas = pd.read_sql_query(
        "SELECT * FROM salas ORDER BY nome",
        conexao
    )

    conexao.close()

    if professores.empty or salas.empty:

        st.warning(
            "É necessário cadastrar pelo menos um professor "
            "e uma sala antes de realizar uma reserva."
        )

    else:

        with st.form("form_reserva"):

            if st.session_state.usuario_tipo == "Professor":

                professor_nome = st.session_state.usuario_nome

                st.text_input(
                    "Professor",
                    value=professor_nome,
                    disabled=True
                )

            else:

                professor_nome = st.selectbox(
                    "Professor",
                    professores["nome"].tolist()
                )

            sala_nome = st.selectbox(
                "Sala",
                salas["nome"].tolist()
            )

            data = st.date_input(
                "Data da reserva"
            )

            col1, col2 = st.columns(2)

            with col1:
                horario_inicio = st.time_input(
                    "Horário de início"
                )

            with col2:
                horario_fim = st.time_input(
                    "Horário de término"
                )

            finalidade = st.text_area(
                "Finalidade da reserva",
                placeholder="Ex.: Aula de Redes de Computadores"
            )

            reservar = st.form_submit_button(
                "Solicitar Reserva"
            )

            if reservar:

                if horario_fim <= horario_inicio:

                    st.error(
                        "O horário de término deve ser posterior "
                        "ao horário de início."
                    )

                elif finalidade.strip() == "":

                    st.warning(
                        "Informe a finalidade da reserva."
                    )

                else:

                    professor_id = int(
                        professores.loc[
                            professores["nome"] == professor_nome,
                            "id"
                        ].iloc[0]
                    )

                    sala_id = int(
                        salas.loc[
                            salas["nome"] == sala_nome,
                            "id"
                        ].iloc[0]
                    )

                    data_texto = data.strftime("%Y-%m-%d")
                    inicio_texto = horario_inicio.strftime("%H:%M")
                    fim_texto = horario_fim.strftime("%H:%M")

                    conexao = sqlite3.connect("reservas.db")
                    cursor = conexao.cursor()

                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM reservas
                        WHERE sala_id = ?
                        AND data = ?
                        AND status NOT IN ('Recusada', 'Cancelada')
                        AND horario_inicio < ?
                        AND horario_fim > ?
                        """,
                        (
                            sala_id,
                            data_texto,
                            fim_texto,
                            inicio_texto
                        )
                    )

                    conflito = cursor.fetchone()[0]

                    if conflito > 0:

                        st.error(
                            "❌ Esta sala já possui uma reserva "
                            "nesse período."
                        )

                    else:

                        cursor.execute(
                            """
                            INSERT INTO reservas
                            (
                                professor_id,
                                sala_id,
                                data,
                                horario_inicio,
                                horario_fim,
                                finalidade,
                                status
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                professor_id,
                                sala_id,
                                data_texto,
                                inicio_texto,
                                fim_texto,
                                finalidade,
                                "Pendente"
                            )
                        )

                        conexao.commit()

                        st.success(
                            "✅ Reserva solicitada com sucesso!"
                        )

                    conexao.close()

    st.divider()

    st.subheader("📋 Reservas realizadas")

    conexao = sqlite3.connect("reservas.db")

    if st.session_state.usuario_tipo == "Professor":

        reservas = pd.read_sql_query(
            """
            SELECT
                reservas.id,
                professores.nome AS professor,
                salas.nome AS sala,
                reservas.data,
                reservas.horario_inicio AS inicio,
                reservas.horario_fim AS fim,
                reservas.finalidade,
                reservas.status
            FROM reservas
            INNER JOIN professores
                ON reservas.professor_id = professores.id
            INNER JOIN salas
                ON reservas.sala_id = salas.id
            WHERE professores.nome = ?
            ORDER BY reservas.data, reservas.horario_inicio
            """,
            conexao,
            params=(st.session_state.usuario_nome,)
        )

    else:

        reservas = pd.read_sql_query(
            """
            SELECT
                reservas.id,
                professores.nome AS professor,
                salas.nome AS sala,
                reservas.data,
                reservas.horario_inicio AS inicio,
                reservas.horario_fim AS fim,
                reservas.finalidade,
                reservas.status
            FROM reservas
            INNER JOIN professores
                ON reservas.professor_id = professores.id
            INNER JOIN salas
                ON reservas.sala_id = salas.id
            ORDER BY reservas.data, reservas.horario_inicio
            """,
            conexao
        )

    conexao.close()

    if reservas.empty:

        st.info("Nenhuma reserva realizada.")

    else:

        st.dataframe(
            reservas,
            width="stretch"
        )

        reservas_ativas = reservas[
            reservas["status"].isin(["Pendente", "Aprovada"])
        ]

        st.divider()
        st.subheader("🚫 Cancelar Reserva")

        if reservas_ativas.empty:

            st.info(
                "Não existem reservas disponíveis para cancelamento."
            )

        else:

            opcoes_reservas = {}

            for _, reserva in reservas_ativas.iterrows():

                descricao = (
                    f"Reserva #{reserva['id']} - "
                    f"{reserva['professor']} - "
                    f"{reserva['sala']} - "
                    f"{reserva['data']} - "
                    f"{reserva['inicio']} às {reserva['fim']}"
                )

                opcoes_reservas[descricao] = int(
                    reserva["id"]
                )

            reserva_selecionada = st.selectbox(
                "Selecione a reserva que deseja cancelar",
                list(opcoes_reservas.keys())
            )

            confirmar_cancelamento = st.checkbox(
                "Confirmo que desejo cancelar esta reserva."
            )

            if st.button(
                "🚫 Cancelar Reserva",
                width="stretch"
            ):

                if not confirmar_cancelamento:

                    st.warning(
                        "Marque a confirmação antes de cancelar."
                    )

                else:

                    reserva_id = opcoes_reservas[
                        reserva_selecionada
                    ]

                    conexao = sqlite3.connect("reservas.db")
                    cursor = conexao.cursor()

                    cursor.execute(
                        """
                        UPDATE reservas
                        SET status = 'Cancelada'
                        WHERE id = ?
                        """,
                        (reserva_id,)
                    )

                    conexao.commit()
                    conexao.close()

                    st.success(
                        "Reserva cancelada com sucesso!"
                    )

                    st.rerun()                       