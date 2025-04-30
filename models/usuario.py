import sqlite3
from utils.helpers import hash_senha

class Usuario:
    def __init__(self, id, nome_completo, email, senha, tipo_usuario, matricula, cpf, data_nascimento):
        self.id = id
        self.nome_completo = nome_completo
        self.email = email
        self.senha = senha
        self.tipo_usuario = tipo_usuario
        self.matricula = matricula
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    @staticmethod
    def buscar_por_matricula(matricula):
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM usuarios WHERE matricula=? OR cpf=?
        ''', (matricula, matricula))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(*row)
        return None

    def verificar_senha(self, senha_digitada):
        from utils.helpers import verificar_senha
        return verificar_senha(self.senha, senha_digitada)

    @staticmethod
    def cadastrar(nome, email, senha, tipo, matricula, cpf, data_nascimento):
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO usuarios (nome_completo, email, senha, tipo_usuario, matricula, cpf, data_nascimento)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nome, email, senha, tipo, matricula, cpf, data_nascimento))
        conn.commit()
        conn.close()