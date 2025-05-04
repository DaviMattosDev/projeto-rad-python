# models/usuario.py
import sqlite3
from datetime import datetime

class AlunoDisciplinaModel:
    def __init__(self):
        self.conn = sqlite3.connect("extensao.db")
        self.cursor = self.conn.cursor()

    def log_debug(self, message):
        with open("debug.txt", "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {message}\n")

    def buscar_aluno_por_matricula(self, matricula):
        """Busca aluno por matrícula."""
        try:
            self.cursor.execute("SELECT id, nome_completo, cpf FROM usuarios WHERE matricula=?", (matricula,))
            return self.cursor.fetchone()
        except Exception as e:
            self.log_debug(f"Erro ao buscar aluno por matrícula: {e}")
            return None

    def buscar_disciplinas(self):
        """Busca todas as disciplinas disponíveis no banco."""
        try:
            self.cursor.execute("SELECT nome FROM disciplinas")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            self.log_debug(f"Erro ao buscar disciplinas: {e}")
            return []

    def buscar_id_disciplina(self, nome_disciplina):
        """Busca o ID da disciplina pelo nome."""
        try:
            self.cursor.execute("SELECT id FROM disciplinas WHERE nome=?", (nome_disciplina,))
            resultado = self.cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            self.log_debug(f"Erro ao buscar disciplina pelo nome: {e}")
            return None

    def verificar_se_aluno_ja_matriculado(self, aluno_id, disciplina_id):
        """Verifica se aluno já está na disciplina."""
        try:
            self.cursor.execute('''
                SELECT * FROM frequencias 
                WHERE aluno_id=? AND disciplina_id=?
            ''', (aluno_id, disciplina_id))
            return self.cursor.fetchone() is not None
        except Exception as e:
            self.log_debug(f"Erro ao verificar aluno na disciplina: {e}")
            return False

    def cadastrar_aluno_na_disciplina(self, aluno_id, disciplina_id):
        """Cadastra o aluno na disciplina."""
        try:
            # Insere o aluno na tabela frequencias com a data atual
            data_atual = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute('''
                INSERT INTO frequencias (aluno_id, disciplina_id, data_aula, presente)
                VALUES (?, ?, ?, ?)
            ''', (aluno_id, disciplina_id, data_atual, False))  # presente=False por padrão
            self.conn.commit()
            return True
        except Exception as e:
            self.log_debug(f"Erro ao cadastrar aluno na disciplina: {e}")
            return False

    def fechar_conexao(self):
        if self.conn:
            self.conn.close()