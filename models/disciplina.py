import sqlite3
from datetime import datetime


class DisciplinaModel:
    def __init__(self):
        self.conn = sqlite3.connect("extensao.db")
        self.cursor = self.conn.cursor()

    def log_debug(self, message):
        """Registra mensagens de debug em 'debug.txt'."""
        with open("debug.txt", "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {message}\n")

    def buscar_professor_por_matricula(self, matricula):
        """Busca o ID do professor com base na matrícula."""
        try:
            self.cursor.execute('''
                SELECT id FROM usuarios WHERE matricula=?
            ''', (matricula,))
            resultado = self.cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            self.log_debug(f"Erro ao buscar professor por matricula: {e}")
            return None

    def cadastrar_disciplina(self, nome, descricao, professor_id):
        """Insere uma nova disciplina no banco de dados."""
        try:
            self.cursor.execute('''
                INSERT INTO disciplinas (nome, descricao, professor_id)
                VALUES (?, ?, ?)
            ''', (nome, descricao, professor_id))
            self.conn.commit()
            return True
        except Exception as e:
            self.log_debug(f"Erro ao cadastrar disciplina: {e}")
            return False

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()