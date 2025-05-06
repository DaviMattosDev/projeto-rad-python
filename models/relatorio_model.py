# models/relatorio_model.py
import sqlite3
from datetime import datetime
from tkinter import messagebox
import openpyxl


class RelatorioModel:
    def __init__(self):
        self.conn = sqlite3.connect("extensao.db")
        self.cursor = self.conn.cursor()

    def log_error(self, error_message):
        with open("debug.txt", "a") as log_file:
            log_file.write(f"[{datetime.now()}] {error_message}\n")

    def buscar_todos_usuarios(self):
        """Busca todos os usuários do sistema."""
        try:
            self.cursor.execute("SELECT id, nome_completo, tipo_usuario, matricula FROM usuarios")
            return self.cursor.fetchall()
        except Exception as e:
            self.log_error(f"Erro ao buscar usuários: {e}")
            return []

    def buscar_disciplinas_com_professores(self):
        """Busca disciplinas com seus respectivos professores."""
        try:
            self.cursor.execute('''
                SELECT d.id, d.nome, u.nome_completo AS professor
                FROM disciplinas d
                LEFT JOIN usuarios u ON d.professor_id = u.id
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            self.log_error(f"Erro ao buscar disciplinas: {e}")
            return []

    def buscar_alunos_por_disciplina(self):
        """Retorna a quantidade de alunos por disciplina."""
        try:
            self.cursor.execute('''
                SELECT d.nome, COUNT(DISTINCT f.aluno_id) AS total_alunos
                FROM disciplinas d
                LEFT JOIN frequencias f ON d.id = f.disciplina_id
                GROUP BY d.id
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            self.log_error(f"Erro ao buscar alunos por disciplina: {e}")
            return []

    def buscar_presencas_por_aluno(self):
        """Calcula a porcentagem de presença dos alunos em cada disciplina."""
        try:
            self.cursor.execute('''
                SELECT u.nome_completo, d.nome,
                    ROUND(
                        (SUM(CASE WHEN f.presente THEN 1 ELSE 0 END) * 100.0) / COUNT(f.id), 2
                    ) AS porcentagem_presenca
                FROM frequencias f
                JOIN usuarios u ON f.aluno_id = u.id
                JOIN disciplinas d ON f.disciplina_id = d.id
                GROUP BY u.id, d.id
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            self.log_error(f"Erro ao buscar presenças: {e}")
            return []

    def buscar_notas_medias(self):
        """Busca média das notas por aluno e disciplina."""
        try:
            self.cursor.execute('''
                SELECT u.nome_completo, d.nome,
                    AVG(n.valor_nota) AS media_nota
                FROM notas n
                JOIN usuarios u ON n.aluno_id = u.id
                JOIN disciplinas d ON n.disciplina_id = d.id
                GROUP BY u.id, d.id
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            self.log_error(f"Erro ao buscar média de notas: {e}")
            return []

    def buscar_total_faltas_por_avaliacao(self):
        """Conta quantos alunos faltaram por avaliação."""
        try:
            self.cursor.execute('''
                SELECT a.descricao, COUNT(*) AS faltas
                FROM notas n
                JOIN avaliacoes a ON n.avaliacao_id = a.id
                WHERE n.faltou = 1
                GROUP BY a.id
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            self.log_error(f"Erro ao contar faltas por avaliação: {e}")
            return []

    def exportar_para_csv(self, dados, cabecalhos, nome_arquivo="relatorio.csv"):
        """Exporta dados para um arquivo CSV."""
        try:
            import csv
            with open(nome_arquivo, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(cabecalhos)
                writer.writerows(dados)
            return True
        except Exception as e:
            self.log_error(f"Erro ao exportar para CSV: {e}")
            return False

    def exportar_para_excel(self, dados, cabecalhos, nome_arquivo="relatorio.xlsx"):
        """Exporta dados para um arquivo Excel (.xlsx)."""
        try:
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(cabecalhos)

            for linha in dados:
                ws.append(linha)

            wb.save(nome_arquivo)
            return True
        except ImportError:
            self.log_error("openpyxl não instalado.")
            messagebox.showwarning("Erro", "A biblioteca 'openpyxl' não está instalada.\nInstale usando 'pip install openpyxl'")
            return False
        except Exception as e:
            self.log_error(f"Erro ao exportar para Excel: {e}")
            return False