import sqlite3
import hashlib
import sys
import os

DB_PATH = "extensao.db"
LOG_FILE = "debug_db.txt"

# Redireciona stdout e stderr para o arquivo de log
class Logger:
    def __init__(self, filename):
        self.log_file = open(filename, 'a', encoding='utf-8')

    def write(self, message):
        self.log_file.write(message)
        self.log_file.flush()

    def flush(self):
        self.log_file.flush()

# Redireciona a saída padrão para o arquivo
sys.stdout = Logger(LOG_FILE)
sys.stderr = Logger(LOG_FILE)

def criar_tabelas():
    conn = None
    try:
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

        # Tabela de Notas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER,
            disciplina_id INTEGER,
            avaliacao_id INTEGER,
            valor_nota REAL,
            faltou BOOLEAN DEFAULT 0,
            FOREIGN KEY(aluno_id) REFERENCES usuarios(id),
            FOREIGN KEY(disciplina_id) REFERENCES disciplinas(id),
            FOREIGN KEY(avaliacao_id) REFERENCES avaliacoes(id)
        )
        ''')

        conn.commit()
        print("✅ Banco de dados criado com todas as tabelas.")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
    finally:
        if conn:
            conn.close()

def criar_admin():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        nome = "Administrador"
        email = "admin@admin.com"
        senha = "admin123"
        tipo_usuario = "admin"
        matricula = "123"
        cpf = "000.000.000-00"
        data_nascimento = "1990-01-01"

        # Criptografar senha com SHA-256
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        cursor.execute('''
        INSERT INTO usuarios (nome_completo, email, senha, tipo_usuario, matricula, cpf, data_nascimento)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, email, senha_hash, tipo_usuario, matricula, cpf, data_nascimento))
        conn.commit()
        print("🔐 Usuário admin criado com sucesso.")
    except sqlite3.IntegrityError:
        print("⚠️ O usuário admin já existe.")
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("\n--- Iniciando inicialização do banco de dados ---")
    criar_tabelas()
    criar_admin()
    print("--- Finalizando inicialização do banco de dados ---\n")