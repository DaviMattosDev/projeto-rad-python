import sqlite3

# Conectar ao banco de dados
def conectar_banco():
    try:
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        print("Conexão com o banco de dados estabelecida.")
        return conn, cursor
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None, None

# Testar consulta para listar funcionários
def testar_listar_funcionarios(cursor):
    print("\n=== Teste: Listar Funcionários ===")
    try:
        cursor.execute("SELECT id, nome, cargo, departamento, situacao, data_inicio FROM funcionarios")
        funcionarios = cursor.fetchall()
        if funcionarios:
            for funcionario in funcionarios:
                print(funcionario)
        else:
            print("Nenhum funcionário encontrado.")
    except Exception as e:
        print(f"Erro ao listar funcionários: {e}")

# Testar consulta para buscar funcionário por username
def testar_buscar_funcionario_por_username(cursor, username):
    print(f"\n=== Teste: Buscar Funcionário por Username ({username}) ===")
    try:
        cursor.execute("""
            SELECT f.id, f.nome 
            FROM usuarios u
            JOIN funcionarios f ON u.funcionario_id = f.id
            WHERE u.username = ?
        """, (username,))
        funcionario = cursor.fetchone()
        if funcionario:
            print(f"Funcionário encontrado: ID={funcionario[0]}, Nome={funcionario[1]}")
        else:
            print("Funcionário não encontrado.")
    except Exception as e:
        print(f"Erro ao buscar funcionário: {e}")

# Testar consulta para listar frequências de um funcionário
def testar_listar_frequencias(cursor, funcionario_id):
    print(f"\n=== Teste: Listar Frequências do Funcionário (ID={funcionario_id}) ===")
    try:
        cursor.execute("""
            SELECT entrada, saida 
            FROM frequencia 
            WHERE funcionario_id = ?
        """, (funcionario_id,))
        frequencias = cursor.fetchall()
        if frequencias:
            for frequencia in frequencias:
                print(f"Entrada: {frequencia[0]}, Saída: {frequencia[1]}")
        else:
            print("Nenhuma frequência encontrada para este funcionário.")
    except Exception as e:
        print(f"Erro ao listar frequências: {e}")

# Testar consulta para obter o último registro de frequência de um funcionário
def testar_obter_ultimo_registro_frequencia(cursor, funcionario_id):
    print(f"\n=== Teste: Obter Último Registro de Frequência (ID={funcionario_id}) ===")
    try:
        cursor.execute("""
            SELECT id, entrada, saida 
            FROM frequencia 
            WHERE funcionario_id = ?
            ORDER BY id DESC LIMIT 1
        """, (funcionario_id,))
        ultimo_registro = cursor.fetchone()
        if ultimo_registro:
            print(f"Último registro: ID={ultimo_registro[0]}, Entrada={ultimo_registro[1]}, Saída={ultimo_registro[2]}")
        else:
            print("Nenhum registro de frequência encontrado para este funcionário.")
    except Exception as e:
        print(f"Erro ao obter último registro: {e}")

# Função principal
def main():
    # Conectar ao banco de dados
    conn, cursor = conectar_banco()
    if not conn or not cursor:
        return

    try:
        # Testar consultas
        testar_listar_funcionarios(cursor)
        testar_buscar_funcionario_por_username(cursor, "davi.mattos")  # Substitua pelo username desejado
        testar_listar_frequencias(cursor, 1)  # Substitua pelo ID do funcionário desejado
        testar_obter_ultimo_registro_frequencia(cursor, 1)  # Substitua pelo ID do funcionário desejado

    finally:
        # Fechar a conexão
        conn.close()
        print("\nConexão com o banco de dados fechada.")

# Executar o script
if __name__ == "__main__":
    main()