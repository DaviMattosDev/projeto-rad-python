import sqlite3
import hashlib

def init_db():
    try:
        # Inicializa a conexão com o banco de dados
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()

        # Tabela de funcionários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cargo TEXT NOT NULL,
                departamento TEXT NOT NULL,
                situacao TEXT NOT NULL,
                data_inicio TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        """)

        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                perfil TEXT NOT NULL,
                funcionario_id INTEGER UNIQUE,
                FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
            )
        """)

        # Tabela de frequência (ponto)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS frequencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                funcionario_id INTEGER NOT NULL,
                entrada TEXT NOT NULL,
                saida TEXT,
                FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
            )
        """)

        # Criar admin se não existir
        cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
        if not cursor.fetchone():
            senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuarios (username, senha, perfil, funcionario_id)
                VALUES (?, ?, ?, ?)
            """, ("admin", senha_hash, "admin", None))

        # Criar gestor se não existir
        cursor.execute("SELECT * FROM usuarios WHERE username = 'gestor'")
        if not cursor.fetchone():
            senha_hash = hashlib.sha256("gestor123".encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuarios (username, senha, perfil, funcionario_id)
                VALUES (?, ?, ?, ?)
            """, ("gestor", senha_hash, "gestor", None))

        # Criar RH se não existir
        cursor.execute("SELECT * FROM usuarios WHERE username = 'rh'")
        if not cursor.fetchone():
            senha_hash = hashlib.sha256("rh123".encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuarios (username, senha, perfil, funcionario_id)
                VALUES (?, ?, ?, ?)
            """, ("rh", senha_hash, "rh", None))

        # Salvar alterações
        conn.commit()

    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

    finally:
        conn.close()


# Executar apenas se este arquivo for o ponto de entrada principal
if __name__ == "__main__":
    print("Iniciando conexão com o banco de dados...")
    init_db()
    print("Conexão bem-sucedida!")
    print("Alterações salvas!")
    print("Conexão com o banco de dados fechada.")