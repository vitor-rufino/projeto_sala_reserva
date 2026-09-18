import sqlite3

def conectar():
    return sqlite3.connect("reservas.db")


def criar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    # Tabela de salas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            capacidade INTEGER NOT NULL,
            localizacao TEXT NOT NULL,
            projetor TEXT NOT NULL,
            computadores INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Disponível'
        )
    """)

    # Tabela de professores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            departamento TEXT NOT NULL
        )
    """)

    # Tabela de reservas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professor_id INTEGER NOT NULL,
            sala_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            horario_inicio TEXT NOT NULL,
            horario_fim TEXT NOT NULL,
            finalidade TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente',

            FOREIGN KEY (professor_id)
                REFERENCES professores(id),

            FOREIGN KEY (sala_id)
                REFERENCES salas(id)
        )
    """)
    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()


def criar_usuarios_iniciais():
    conexao = conectar()
    cursor = conexao.cursor()

    usuarios = [
        (
            "Administrador",
            "admin@faculdade.com",
            "1234",
            "Administrador"
        ),
        (
            "João da Silva",
            "joao@faculdade.com",
            "1234",
            "Professor"
        )
    ]

    for usuario in usuarios:
        try:
            cursor.execute(
                """
                INSERT INTO usuarios
                (nome, email, senha, tipo)
                VALUES (?, ?, ?, ?)
                """,
                usuario
            )
        except sqlite3.IntegrityError:
            pass

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_banco()
    criar_usuarios_iniciais()
    print("Banco de dados atualizado com sucesso!")