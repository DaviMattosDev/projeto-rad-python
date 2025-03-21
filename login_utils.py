import sqlite3


def verificar_login(usuario, senha):
    # Conexão com o banco de dados
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()

    # Consulta para verificar o login
    cursor.execute('''
    SELECT id, perfil FROM usuarios WHERE usuario = ? AND senha = ?
    ''', (usuario, senha))
    resultado = cursor.fetchone()  # Retorna uma tupla (id, perfil) ou None

    conn.close()

    if resultado:
        print(
            f"Login bem-sucedido para o usuário: {usuario} (Perfil: {resultado[1]})")
        return resultado  # Retorna (id, perfil)
    else:
        print("Falha no login: Usuário ou senha inválidos.")
        return None
