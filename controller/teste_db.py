import sqlite3

def conectar_banco():
    """Conecta ao banco de dados SQLite e retorna a conexão."""
    try:
        conn = sqlite3.connect("sistema.db")
        print("Conexão com o banco de dados estabelecida.")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def listar_tabelas(conn):
    """Lista todas as tabelas no banco de dados."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()
        if tabelas:
            print("Tabelas encontradas:")
            for tabela in tabelas:
                print(f"- {tabela[0]}")
        else:
            print("Nenhuma tabela encontrada no banco de dados.")
    except Exception as e:
        print(f"Erro ao listar tabelas: {e}")

def exibir_dados_tabela(conn, tabela):
    """Exibe todos os dados de uma tabela específica."""
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({tabela});")
        colunas = [coluna[1] for coluna in cursor.fetchall()]
        print(f"\nColunas da tabela '{tabela}': {', '.join(colunas)}")

        cursor.execute(f"SELECT * FROM {tabela};")
        dados = cursor.fetchall()
        if dados:
            print(f"Dados da tabela '{tabela}':")
            for linha in dados:
                print(linha)
        else:
            print(f"A tabela '{tabela}' está vazia.")
    except Exception as e:
        print(f"Erro ao exibir dados da tabela '{tabela}': {e}")

def inserir_dados_teste(conn):
    """Insere dados de teste nas tabelas para validação."""
    try:
        cursor = conn.cursor()

        # Inserir funcionário de teste
        cursor.execute("""
            INSERT INTO funcionarios (nome, cargo, departamento, situacao, data_inicio, senha)
            VALUES ('Teste Silva', 'Analista de Testes', 'TI', 'presencial', '2023-10-01', 'teste123');
        """)
        funcionario_id = cursor.lastrowid

        # Inserir usuário de teste
        cursor.execute("""
            INSERT INTO usuarios (username, senha, perfil, funcionario_id)
            VALUES ('teste.silva', 'hash_senha_teste', 'funcionario', ?);
        """, (funcionario_id,))

        # Inserir frequência de teste
        cursor.execute("""
            INSERT INTO frequencia (funcionario_id, entrada, saida)
            VALUES (?, '2023-10-01 08:00:00', '2023-10-01 17:00:00');
        """, (funcionario_id,))

        conn.commit()
        print("Dados de teste inseridos com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir dados de teste: {e}")

def limpar_dados_teste(conn):
    """Remove os dados de teste inseridos."""
    try:
        cursor = conn.cursor()

        # Remover frequência de teste
        cursor.execute("DELETE FROM frequencia WHERE funcionario_id IN (SELECT id FROM funcionarios WHERE nome = 'Teste Silva');")

        # Remover usuário de teste
        cursor.execute("DELETE FROM usuarios WHERE username = 'teste.silva';")

        # Remover funcionário de teste
        cursor.execute("DELETE FROM funcionarios WHERE nome = 'Teste Silva';")

        conn.commit()
        print("Dados de teste removidos com sucesso!")
    except Exception as e:
        print(f"Erro ao limpar dados de teste: {e}")

def menu_principal():
    """Menu principal para interação com o usuário."""
    conn = conectar_banco()
    if not conn:
        return

    while True:
        print("\n=== Menu de Testes ===")
        print("1. Listar tabelas")
        print("2. Exibir dados de uma tabela")
        print("3. Inserir dados de teste")
        print("4. Limpar dados de teste")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_tabelas(conn)
        elif opcao == "2":
            tabela = input("Digite o nome da tabela: ")
            exibir_dados_tabela(conn, tabela)
        elif opcao == "3":
            inserir_dados_teste(conn)
        elif opcao == "4":
            limpar_dados_teste(conn)
        elif opcao == "5":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

    conn.close()

if __name__ == "__main__":
    menu_principal()