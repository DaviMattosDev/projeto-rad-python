import sqlite3
from datetime import datetime
import hashlib
import random

DB_PATH = "extensao.db"

# Funções auxiliares
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def gerar_matricula():
    ano = datetime.now().strftime("%Y")
    mes = datetime.now().strftime("%m")
    numero_aleatorio = str(random.randint(0, 999)).zfill(3)
    return f"{ano}{mes}{numero_aleatorio}"

def gerar_senha_bruta(data_nascimento, cpf):
    data_formatada = ''.join(filter(str.isdigit, data_nascimento))[:8]  # DDMMYYYY
    ultimos_3_cpf = cpf.replace('.', '').replace('-', '')[-3:]  # Remove formatação e pega últimos 3 dígitos
    return f"{data_formatada}{ultimos_3_cpf}"

def gerar_senha_padrao(data_nascimento, cpf):
    senha_bruta = gerar_senha_bruta(data_nascimento, cpf)
    return hash_senha(senha_bruta)

# Dados dos usuários exemplo
usuarios_data = [
    {
        "nome_completo": "João da Silva",
        "email": "joao.silva@example.com",
        "cpf": "222.222.222-22",
        "data_nascimento": "15/05/1975",
        "tipo_usuario": "professor"
    },
    {
        "nome_completo": "Maria Oliveira",
        "email": "maria.oliveira@example.com",
        "cpf": "333.333.333-33",
        "data_nascimento": "10/10/2000",
        "tipo_usuario": "aluno"
    }
]

# Conectar ao banco
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # Criando admin manualmente primeiro
    for usuario in usuarios_data:
        matricula = gerar_matricula()
        senha_bruta = gerar_senha_bruta(usuario["data_nascimento"], usuario["cpf"])
        senha_hash = gerar_senha_padrao(usuario["data_nascimento"], usuario["cpf"])

        cursor.execute('''
        INSERT INTO usuarios (nome_completo, email, senha, tipo_usuario, matricula, cpf, data_nascimento)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            usuario["nome_completo"],
            usuario["email"],
            senha_hash,
            usuario["tipo_usuario"],
            matricula,
            usuario["cpf"],
            usuario["data_nascimento"]
        ))
        print(f"✅ {usuario['tipo_usuario'].capitalize()} criado(a) - Matrícula: {matricula} | Senha inicial: {senha_bruta}")

    # Confirmar aluno_id e professor_id inseridos
    cursor.execute("SELECT id FROM usuarios WHERE cpf=?", ("222.222.222-22",))
    professor_id = cursor.fetchone()[0]

    # Inserir disciplina RAD
    cursor.execute('''
    INSERT INTO disciplinas (nome, descricao, professor_id)
    VALUES (?, ?, ?)
    ''', ("RAD", "Desenvolvimento Ágil de Aplicações", professor_id))
    print("✅ Disciplina 'RAD' criada e vinculada ao professor.")

    conn.commit()
    print("\n🎉 Todos os registros foram inseridos com sucesso!")

except Exception as e:
    print(f"\n❌ Erro ao inserir dados: {e}")
    conn.rollback()

finally:
    conn.close()