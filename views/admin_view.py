import tkinter as tk
from tkinter import ttk
from views.cadastrar_usuario_view import CadastrarUsuarioView
from views.cadastrar_disciplina_view import CadastrarDisciplinaView
from views.cadastrar_aluno_disciplina_view import CadastrarAlunoDisciplinaView
from views.trocar_senha_view import TrocarSenhaView
from views.remover_matricula_view import RemoverAlunoProfessorView
from views.relatorios_view import RelatoriosView
from views.desmatricular_view import DesmatricularUsuarioView

import traceback


class AdminView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Administração")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        self.centralizar_janela(self.root, 800, 600)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0056b3")])
        style.configure("TLabel", font=("Arial", 14), background="#f5f5f5")
        style.configure("TFrame", background="#f5f5f5")

        title_frame = ttk.Frame(self.root, style="TFrame")
        title_frame.pack(pady=20)
        ttk.Label(title_frame, text="Painel do Administrador", style="TLabel").pack()

        button_frame = ttk.Frame(self.root, style="TFrame")
        button_frame.pack(pady=20)

        buttons = [
            ("Cadastrar Aluno", self.cadastrar_aluno),
            ("Cadastrar Professor", self.cadastrar_professor),
            ("Cadastrar Disciplina", self.cadastrar_disciplina),
            ("Cadastrar Aluno em Disciplina", self.cadastrar_aluno_disciplina),
            ("Desmatricular Aluno/Professor", self.desmatricular_aluno_professor),
            ("Relatórios", self.relatorios),
            ("Remover Aluno de Professor", self.remover_aluno_professor),
            ("Trocar Senha", self.trocar_senha),
            ("Deslogar", self.logout)
        ]

        for text, command in buttons:
            ttk.Button(button_frame, text=text, command=command, style="TButton").pack(fill=tk.X, pady=5, padx=20)

    def centralizar_janela(self, janela, largura, altura):
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2
        janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def log_erro(self, nome_funcao):
        with open("debug.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[ERRO em {nome_funcao}]\n")
            f.write(traceback.format_exc())
            f.write("\n")

    def logout(self):
        try:
            self.root.destroy()
            from controllers.auth_controller import AuthController
            auth = AuthController()
            auth.start()
        except Exception:
            self.log_erro("logout")

    def cadastrar_aluno(self):
        try:
            view = CadastrarUsuarioView("aluno")
            self.centralizar_janela(view.root, 500, 400)
        except Exception:
            self.log_erro("cadastrar_aluno")

    def cadastrar_professor(self):
        try:
            view = CadastrarUsuarioView("professor")
            self.centralizar_janela(view.root, 500, 400)
        except Exception:
            self.log_erro("cadastrar_professor")

    def cadastrar_disciplina(self):
        try:
            view = CadastrarDisciplinaView(self.root)
            self.centralizar_janela(view.root, 500, 500)
            view.root.lift()
            view.root.focus_force()
        except Exception:
            self.log_erro("cadastrar_disciplina")

    def cadastrar_aluno_disciplina(self):
        try:
            view = CadastrarAlunoDisciplinaView()
            self.centralizar_janela(view.root, 500, 600)
        except Exception:
            self.log_erro("cadastrar_aluno_disciplina")

    def desmatricular_aluno_professor(self):
        try:
            view = DesmatricularUsuarioView(self.root)
            self.centralizar_janela(view.root, 500, 400)
        except Exception as e:
            self.log_erro("desmatricular_aluno_professor")        

    def relatorios(self):
        try:
            view = RelatoriosView()
            self.centralizar_janela(view.root, 800, 600)
        except Exception:
            self.log_erro("relatorios")

    def trocar_senha(self):
        try:
            view = TrocarSenhaView()
            self.centralizar_janela(view.root, 400, 300)
        except Exception:
            self.log_erro("trocar_senha")

    def remover_aluno_professor(self):
        try:
            view = RemoverAlunoProfessorView()
            self.centralizar_janela(view.root, 500, 400)
        except Exception:
            self.log_erro("remover_aluno_professor")

    def start(self):
        try:
            self.root.mainloop()
        except Exception:
            self.log_erro("start")
