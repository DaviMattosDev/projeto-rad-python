# models/disciplina.py

from datetime import datetime
import sqlite3


class DisciplinaModel:
    def __init__(self):
        self.conn = sqlite3.connect("extensao.db")
        self.cursor = self.conn.cursor()

    def log_debug(self, error_message):
        """Grava mensagens de erro no arquivo debug.txt"""
        with open("debug.txt", "a") as log_file:
            log_file.write(f"[{datetime.now()}] {error_message}\n")

    def buscar_todas_disciplinas(self):
        """Retorna todas as disciplinas como [(nome, id)]"""
        try:
            self.cursor.execute("SELECT nome, id FROM disciplinas")
            return self.cursor.fetchall()
        except Exception as e:
            self.log_debug(f"buscar_todas_disciplinas: {e}")
            return []

    def buscar_professor_por_matricula(self, matricula):
        """Busca o ID e nome do professor pela matrícula."""
        try:
            self.cursor.execute("""
                SELECT id, nome_completo FROM usuarios
                WHERE tipo_usuario='professor' AND matricula=?
            """, (matricula,))
            return self.cursor.fetchone()
        except Exception as e:
            self.log_debug(f"buscar_professor_por_matricula: {e}")
            return None

    def buscar_disciplina_do_professor(self, professor_id):
        """Retorna a disciplina atual do professor (se houver)."""
        try:
            self.cursor.execute("SELECT id, nome FROM disciplinas WHERE professor_id=?", (professor_id,))
            return self.cursor.fetchone()
        except Exception as e:
            self.log_debug(f"buscar_disciplina_do_professor: {e}")
            return None

    def cadastrar_disciplina(self, nome, descricao, professor_id):
        """Cadastra ou atualiza a disciplina do professor."""
        try:
            # Se o professor já tiver disciplina, remove ele da antiga
            self.cursor.execute("UPDATE disciplinas SET professor_id=NULL WHERE professor_id=?", (professor_id,))

            # Cadastra na nova disciplina
            self.cursor.execute('''
                INSERT INTO disciplinas (nome, descricao, professor_id)
                VALUES (?, ?, ?)
            ''', (nome, descricao or "", professor_id))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            self.log_debug(f"cadastrar_disciplina: {e}")
            return False