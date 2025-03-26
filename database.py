import sqlite3
import hashlib

def init_db():
    try:
        print("Iniciando conexão com o banco de dados...")
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        print("Conexão bem-sucedida!")

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
        print("Tabela 'funcionarios' criada!")

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

        """print("Tabela 'usuarios' criada!")"""

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
        '''print("Tabela 'frequencia' criada!")'''

        # Criar admin se não existir
        cursor.execute("SELECT * FROM usuarios WHERE username = 'admin'")
        if not cursor.fetchone():
            senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuarios (username, senha, perfil, funcionario_id)
                VALUES (?, ?, ?, ?)
            """, ("admin", senha_hash, "admin", None))
            print("Usuário 'admin' criado!")

        # Criar gestor se não existir
        cursor.execute("SELECT * FROM usuarios WHERE username = 'gestor'")
        if not cursor.fetchone():
            senha_hash = hashlib.sha256("gestor123".encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuarios (username, senha, perfil, funcionario_id)
                VALUES (?, ?, ?, ?)
            """, ("gestor", senha_hash, "gestor", None))
            print("Usuário 'gestor' criado!")

        # Criar RH se não existir
        cursor.execute("SELECT * FROM usuarios WHERE username = 'rh'")
        if not cursor.fetchone():
            senha_hash = hashlib.sha256("rh123".encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuarios (username, senha, perfil, funcionario_id)
                VALUES (?, ?, ?, ?)
            """, ("rh", senha_hash, "rh", None))
            print("Usuário 'rh' criado!")

        # Salvar alterações
        conn.commit()
        print("Alterações salvas!")

    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

    finally:
        conn.close()
        print("Conexão com o banco de dados fechada.")


'''if __name__ == "__main__":
    init_db()'''