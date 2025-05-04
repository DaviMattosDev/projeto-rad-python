# models/professor_model.py
from datetime import datetime
import sqlite3

class ProfessorModel:
    def __init__(self, professor_id):
        self.professor_id = professor_id
        self.alunos = []
        self.avaliacoes = []
        self.disciplinas = []

    def log_error(self, error_message):
        with open("debug.txt", "a") as log:
            log.write(f"[{datetime.now()}] {error_message}\n")

    def buscar_alunos_do_professor(self):
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT u.id, u.nome_completo 
                FROM usuarios u
                JOIN frequencias f ON u.id = f.aluno_id
                JOIN disciplinas d ON f.disciplina_id = d.id
                WHERE d.professor_id=?
            ''', (self.professor_id,))
            self.alunos = cursor.fetchall()
            conn.close()
            return self.alunos
        except Exception as e:
            self.log_error(f"buscar_alunos_do_professor: {e}")
            return []

    def verificar_presenca(self, aluno_id, data_aula):
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute("SELECT presente FROM frequencias WHERE aluno_id=? AND data_aula=?", (aluno_id, data_aula))
            row = cursor.fetchone()
            conn.close()
            return row[0] if row else False
        except Exception as e:
            self.log_error(f"verificar_presenca: {e}")
            return False

    def registrar_presenca(self, aluno_id, data_aula, presente):
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM frequencias WHERE aluno_id=? AND data_aula=?", (aluno_id, data_aula))
            row = cursor.fetchone()

            if row:
                cursor.execute("UPDATE frequencias SET presente=? WHERE aluno_id=? AND data_aula=?", (presente, aluno_id, data_aula))
            else:
                cursor.execute('''
                    INSERT INTO frequencias (aluno_id, disciplina_id, data_aula, presente)
                    VALUES (?, ?, ?, ?)
                ''', (aluno_id, 1, data_aula, presente))  # Substituir 1 pela disciplina certa após seleção real
            conn.commit()
            conn.close()
        except Exception as e:
            self.log_error(f"registrar_presenca: {e}")

    def salvar_nota(self, aluno_id, avaliacao_id, valor_nota=None, faltou=False):
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            if faltou:
                cursor.execute('''
                    INSERT INTO notas (aluno_id, disciplina_id, avaliacao_id, faltou)
                    VALUES (?, ?, ?, ?)
                ''', (aluno_id, 1, avaliacao_id, True))
            else:
                cursor.execute('''
                    INSERT INTO notas (aluno_id, disciplina_id, avaliacao_id, valor_nota)
                    VALUES (?, ?, ?, ?)
                ''', (aluno_id, 1, avaliacao_id, valor_nota))
            conn.commit()
            conn.close()
        except Exception as e:
            self.log_error(f"salvar_nota: {e}")

    def buscar_avaliacao(self, tipo_avaliacao):
        """Busca avaliação ativa pelo tipo."""
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id FROM avaliacoes
                WHERE tipo_avaliacao=? AND disciplina_id=?
            ''', (tipo_avaliacao, self.disciplina_selecionada))
            row = cursor.fetchone()
            conn.close()
            return row if row else None
        except Exception as e:
            self.log_error(f"buscar_avaliacao: {e}")
            return None

    def atualizar_disciplinas(self):
        """Atualiza a lista de disciplinas do professor."""
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM disciplinas WHERE professor_id=?", (self.professor_id,))
            self.disciplinas = cursor.fetchall()
            conn.close()
        except Exception as e:
            self.log_error(f"atualizar_disciplinas: {e}")

    def definir_disciplina_selecionada(self, disciplina_id):
        """Define qual disciplina está sendo usada."""
        self.disciplina_selecionada = disciplina_id

    def atualizar_disciplinas_e_avaliacoes(self):
        self.atualizar_disciplinas()
        self.alunos = self.buscar_alunos_do_professor()

    def buscar_avaliacoes_futuras(self):
        """Retorna apenas avaliações com data >= hoje."""
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.id, d.nome, a.data_avaliacao, a.descricao, a.tipo_avaliacao
                FROM avaliacoes a
                JOIN disciplinas d ON a.disciplina_id = d.id
                WHERE d.professor_id=?
            ''', (self.professor_id,))
            todas_avaliacoes = cursor.fetchall()
            conn.close()
            data_atual = datetime.now().date()
            avaliacoes_filtradas = [
                a for a in todas_avaliacoes
                if datetime.strptime(a[2], "%Y-%m-%d").date() >= data_atual
            ]
            self.avaliacoes = avaliacoes_filtradas
            return self.avaliacoes
        except Exception as e:
            self.log_error(f"buscar_avaliacoes_futuras: {e}")
            return []

    def criar_avaliacao(self, descricao, data_avaliacao, tipo_avaliacao):
        """Cria uma nova avaliação no banco de dados."""
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO avaliacoes (disciplina_id, data_avaliacao, descricao, tipo_avaliacao)
                VALUES (?, ?, ?, ?)
            ''', (self.disciplina_selecionada, data_avaliacao, descricao, tipo_avaliacao))
            conn.commit()
            conn.close()
        except Exception as e:
            self.log_error(f"criar_avaliacao: {e}")

    def contar_alunos_aprovados(self, avaliacao_id):
        """Conta os alunos aprovados em uma avaliação."""
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM notas
                WHERE avaliacao_id=? AND valor_nota >= 6
            ''', (avaliacao_id,))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            self.log_error(f"contar_alunos_aprovados: {e}")
            return 0

    def contar_faltas(self, avaliacao_id):
        """Conta os alunos que faltaram em uma avaliação."""
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM notas
                WHERE avaliacao_id=? AND faltou=1
            ''', (avaliacao_id,))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            self.log_error(f"contar_faltas: {e}")
            return 0