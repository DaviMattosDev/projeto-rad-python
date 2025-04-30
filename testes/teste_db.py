import sqlite3

DB_PATH = "extensao.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Ver todos os usuários (sem senha original - só o hash)
cursor.execute("SELECT matricula, nome_completo, cpf, data_nascimento FROM usuarios")
usuarios = cursor.fetchall()

print("\nUsuarios no banco:")
for user in usuarios:
    matricula, nome, cpf, data_nascimento = user

    # Gera a senha bruta com base nos campos originais
    data_formatada = ''.join(filter(str.isdigit, data_nascimento))[:8]
    ultimos_digitos_cpf = cpf.replace('.', '').replace('-', '')[-3:]
    senha_bruta = data_formatada + ultimos_digitos_cpf

    print(f"\nNome: {nome}")
    print(f"Matrícula: {matricula}")
    print(f"CPF: {cpf}")
    print(f"Data Nasc: {data_nascimento}")
    print(f"Senha Inicial: {senha_bruta}")