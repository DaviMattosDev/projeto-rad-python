import sqlite3
from datetime import datetime


class DesmatricularModel:
    def __init__(self):
        self.conn = sqlite3.connect("extensao.db")
        self.cursor = self.conn.cursor()

    def buscar_por_matricula(self, matricula):
        try:
            self.cursor.execute('''
                SELECT id, nome_completo, tipo_usuario 
                FROM usuarios 
                WHERE matricula=? OR cpf=?
            ''', (matricula, matricula))
            resultado = self.cursor.fetchone()
            if resultado:
                return {
                    "id": resultado[0],
                    "nome_completo": resultado[1],
                    "tipo_usuario": resultado[2]
                }
            return None
        except Exception as e:
            self.log_error(f"buscar_por_matricula: {e}")
            return None

    def desmatricular_usuario(self, matricula):
        try:
            self.cursor.execute('''
                DELETE FROM usuarios 
                WHERE matricula=? OR cpf=?
            ''', (matricula, matricula))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            self.conn.rollback()
            self.log_error(f"desmatricular_usuario: {e}")
            return False

    def log_error(self, error_message):
        with open("debug.txt", "a") as f:
            f.write(f"[{datetime.now()}] {error_message}\n")

    def fechar_conexao(self):
        self.conn.close()