# models/remover_aluno_professor_model.py

from datetime import datetime
import sqlite3


class RemoverAlunoProfessorModel:
    def __init__(self):
        self.conn = sqlite3.connect("extensao.db")
        self.cursor = self.conn.cursor()

    def log_error(self, error_message):
        with open("debug.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}: {error_message}\n")

    def buscar_professores(self):
        """Busca todos os professores."""
        try:
            self.cursor.execute("SELECT nome_completo, id FROM usuarios WHERE tipo_usuario = 'professor'")
            return self.cursor.fetchall()
        except Exception as e:
            self.log_error(f"buscar_professores: {e}")
            return []

    def buscar_disciplinas_do_professor(self, professor_id):
        """Busca as disciplinas ministradas por um professor."""
        try:
            self.cursor.execute("SELECT id, nome FROM disciplinas WHERE professor_id=?", (professor_id,))
            return self.cursor.fetchall()
        except Exception as e:
            self.log_error(f"buscar_disciplinas_do_professor: {e}")
            return []

    def buscar_alunos_da_disciplina(self, disciplina_id):
        """Busca os alunos matriculados em uma disciplina (usando campo 'matricula')."""
        try:
            self.cursor.execute('''
                SELECT u.id, u.matricula 
                FROM usuarios u
                JOIN frequencias f ON u.id = f.aluno_id
                WHERE f.disciplina_id = ?
            ''', (disciplina_id,))
            return self.cursor.fetchall()
        except Exception as e:
            self.log_error(f"buscar_alunos_da_disciplina: {e}")
            return []

    def aluno_esta_na_disciplina(self, aluno_id, disciplina_id):
        """Verifica se o aluno está presente na disciplina."""
        try:
            self.cursor.execute('''
                SELECT COUNT(*) FROM frequencias
                WHERE aluno_id = ? AND disciplina_id = ?
            ''', (aluno_id, disciplina_id))
            resultado = self.cursor.fetchone()[0]
            return resultado > 0
        except Exception as e:
            self.log_error(f"aluno_esta_na_disciplina: {e}")
            return False

    def remover_aluno_de_professor(self, professor_id, aluno_id, disciplina_id=None):
        """
        Remove um aluno da lista de alunos do professor.
        Se disciplina_id for fornecido, verifica se o aluno está nessa disciplina antes de deletar.
        """
        if disciplina_id is not None and not self.aluno_esta_na_disciplina(aluno_id, disciplina_id):
            self.log_error(f"Aluno ID {aluno_id} não está matriculado na disciplina ID {disciplina_id}.")
            return False

        try:
            self.cursor.execute("""
                DELETE FROM matriculas
                WHERE professor_id = ? AND aluno_id = ?
            """, (professor_id, aluno_id))
            self.conn.commit()
            return True
        except Exception as e:
            self.log_error(f"remover_aluno_de_professor: {e}")
            return False