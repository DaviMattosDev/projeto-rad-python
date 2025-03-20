def verificar_login(usuario, senha):
    # Usuários autorizados (pode ser substituído por um banco de dados de usuários no futuro)
    usuarios_autorizados = {
        "admin": "senha123",
        "gerente": "gestao123",
        "rh": "123"
    }
    return usuarios_autorizados.get(usuario) == senha