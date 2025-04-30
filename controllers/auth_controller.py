from views.login_view import LoginView
from models.usuario import Usuario

# auth_controller.py
class AuthController:
    def __init__(self):
        self.view = LoginView(self)

    def login(self):
        matricula, senha = self.view.get_dados_login()
        open("debug.txt", "w").close()  # Limpa o conteúdo do arquivo debug.txt
        # Gravar logs no arquivo debug.txt
        with open("debug.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"[DEBUG] Matrícula digitada: '{matricula}'\n")
            log_file.write(f"[DEBUG] Senha digitada (texto): '{senha}'\n")

            usuario = Usuario.buscar_por_matricula(matricula)

            if usuario:
                log_file.write(f"[DEBUG] Usuário encontrado: {usuario.nome_completo}\n")
                log_file.write(f"[DEBUG] Tipo de usuário: {usuario.tipo_usuario}\n")
                log_file.write(f"[DEBUG] Senha no banco (hash armazenado): {usuario.senha}\n")

                senha_verificada = usuario.verificar_senha(senha)
                log_file.write(f"[DEBUG] Resultado da verificação da senha: {senha_verificada}\n")
            else:
                log_file.write(f"[DEBUG] Nenhum usuário encontrado com a matrícula: '{matricula}'\n")

        # Verificar credenciais e redirecionar o usuário
        if usuario and usuario.verificar_senha(senha):  # Verifica a senha digitada
            self.view.root.destroy()
            if usuario.tipo_usuario == 'admin':
                from views.admin_view import AdminView
                AdminView().start()
            elif usuario.tipo_usuario == 'professor':
                from views.professor_view import ProfessorView
                ProfessorView(usuario).start()
            else:
                from views.aluno_view import AlunoView
                AlunoView(usuario).start()
        else:
            self.view.mostrar_erro("Matrícula ou senha inválida.")

    def start(self):
        self.view.start()