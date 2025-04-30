import sqlite3

DB_PATH = "extensao.db"

def criar_tabelas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela de Usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo_usuario TEXT NOT NULL CHECK(tipo_usuario IN ('admin', 'professor', 'aluno')),
        matricula TEXT NOT NULL UNIQUE,
        cpf TEXT NOT NULL,
        data_nascimento DATE NOT NULL
    )
    ''')

    # Tabela de Disciplinas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        professor_id INTEGER,
        FOREIGN KEY(professor_id) REFERENCES usuarios(id)
    )
    ''')

    # Tabela de Frequências
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS frequencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        disciplina_id INTEGER,
        data_aula DATE NOT NULL,
        presente BOOLEAN NOT NULL,
        FOREIGN KEY(aluno_id) REFERENCES usuarios(id),
        FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id)
    )
    ''')

    # Tabela de Notas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        disciplina_id INTEGER,
        avaliacao_id INTEGER,
        valor_nota REAL,
        faltou BOOLEAN DEFAULT 0, -- Novo campo: 1 para falta, 0 para presença
        FOREIGN KEY(aluno_id) REFERENCES usuarios(id),
        FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id),
        FOREIGN KEY(avaliacao_id) REFERENCES avaliacoes(id)
        )
    ''')

    # Tabela de Avaliações
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disciplina_id INTEGER,
        data_avaliacao DATE NOT NULL,
        descricao TEXT,
        tipo_avaliacao TEXT,
        FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("✅ Banco de dados criado com todas as tabelas.")

if __name__ == "__main__":
    criar_tabelas()