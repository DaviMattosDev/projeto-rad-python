from views.login_view import LoginView
from models.usuario import Usuario


class AuthController:
    def __init__(self):
        self.view = None

    def start(self):
        """Inicia a tela de login e centraliza ela."""
        self.view = LoginView(self)
        self.centralizar_janela(self.view.root, 500, 400) 
        self.view.start()

    def centralizar_janela(self, janela, largura, altura):
        """Centraliza uma janela na tela."""
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2
        janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def login(self):
        matricula, senha = self.view.get_dados_login()
        open("debug.txt", "w").close()  # Limpa logs anteriores

        with open("debug.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"[DEBUG] Matrícula digitada: '{matricula}'\n")
            log_file.write(f"[DEBUG] Senha digitada (texto): '{senha}'\n")

        usuario = Usuario.buscar_por_matricula(matricula)

        with open("debug.txt", "a", encoding="utf-8") as log_file:
            if not usuario:
                log_file.write(f"[DEBUG] Nenhum usuário encontrado com a matrícula: '{matricula}'\n")
            else:
                log_file.write(f"[DEBUG] Usuário encontrado: {usuario.nome_completo}\n")
                log_file.write(f"[DEBUG] Tipo de usuário: {usuario.tipo_usuario}\n")
                log_file.write(f"[DEBUG] Senha no banco (hash armazenado): {usuario.senha}\n")
                log_file.write(f"[DEBUG] Resultado da verificação da senha: {usuario.verificar_senha(senha)}\n")

        if usuario and usuario.verificar_senha(senha):
            self.view.root.destroy()
            if usuario.tipo_usuario == 'admin':
                from views.admin_view import AdminView
                AdminView().start()
            elif usuario.tipo_usuario == 'professor':
                from views.professor_view import ProfessorView
                ProfessorView(usuario).start()
            elif usuario.tipo_usuario == 'aluno':
                from views.aluno_view import AlunoView
                AlunoView(usuario).start()
        else:
            self.view.mostrar_erro("Matrícula ou senha inválida.")
