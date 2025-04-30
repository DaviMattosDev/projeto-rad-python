import hashlib
import random
from datetime import datetime

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(hash_armazenado, senha_digitada):
    return hash_armazenado == hash_senha(senha_digitada)

def gerar_matricula():
    ano = datetime.now().strftime("%Y")
    mes = datetime.now().strftime("%m")
    numero_aleatorio = str(random.randint(0, 999)).zfill(3)
    return f"{ano}{mes}{numero_aleatorio}"

def gerar_senha_bruta(data_nascimento, cpf):
    """Gera a senha inicial em texto puro baseada na data de nascimento e CPF."""
    data_formatada = ''.join(filter(str.isdigit, data_nascimento))[:8]  # DDMMYYYY
    cpf_limpo = ''.join(filter(str.isdigit, cpf))  # Remove pontos e traços
    ultimos_3_cpf = cpf_limpo[-3:]  # Pega os últimos 3 dígitos do CPF
    return f"{data_formatada}{ultimos_3_cpf}"

def gerar_senha_padrao(data_nascimento, cpf):
    """Gera a senha inicial EM TEXTO PURO (não aplica hash aqui)."""
    return gerar_senha_bruta(data_nascimento, cpf)
