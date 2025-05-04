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

    @staticmethod
    def trocar_senha(matricula, nova_senha):
        """
        Atualiza a senha do usuário com base na matrícula ou CPF.
        Retorna True se a atualização for bem-sucedida, False caso contrário.
        """
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            
            # Busca o usuário pela matrícula ou pelo CPF
            cursor.execute('''
            SELECT id FROM usuarios WHERE matricula=? OR cpf=?
            ''', (matricula, matricula))
            resultado = cursor.fetchone()

            if not resultado:
                raise ValueError("Usuário não encontrado.")

            usuario_id = resultado[0]
            senha_hash = hash_senha(nova_senha)

            cursor.execute('''
            UPDATE usuarios SET senha=? WHERE id=?
            ''', (senha_hash, usuario_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            from datetime import datetime
            with open("debug.txt", "a") as log_file:
                log_file.write(f"[{datetime.now()}] Erro ao trocar senha: {e}\n")
            return False