import tkinter as tk
from tkinter import ttk
from views.cadastrar_usuario_view import CadastrarUsuarioView
from views.cadastrar_disciplina_view import CadastrarDisciplinaView
from views.cadastrar_aluno_disciplina_view import CadastrarAlunoDisciplinaView


class AdminView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Administração")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        # Centralizar a janela principal
        self.centralizar_janela(self.root, 800, 600)

        # Configuração do estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0056b3")])
        style.configure("TLabel", font=("Arial", 14), background="#f5f5f5")
        style.configure("TFrame", background="#f5f5f5")

        # Título principal
        title_frame = ttk.Frame(self.root, style="TFrame")
        title_frame.pack(pady=20)
        ttk.Label(title_frame, text="Painel do Administrador", style="TLabel").pack()

        # Frame para os botões
        button_frame = ttk.Frame(self.root, style="TFrame")
        button_frame.pack(pady=20)

        # Botões com design melhorado
        buttons = [
            ("Cadastrar Aluno", self.cadastrar_aluno),
            ("Cadastrar Professor", self.cadastrar_professor),
            ("Cadastrar Disciplina", self.cadastrar_disciplina),
            ("Cadastrar Aluno em Disciplina", self.cadastrar_aluno_disciplina)
        ]

        for text, command in buttons:
            ttk.Button(button_frame, text=text, command=command, style="TButton").pack(fill="x", pady=5, padx=20)

    def centralizar_janela(self, janela, largura, altura):
        """Centraliza uma janela na tela."""
        # Obter as dimensões da tela
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()

        # Calcular as coordenadas x e y para centralizar a janela
        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2

        # Definir a geometria da janela
        janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def cadastrar_aluno(self):
        from views.cadastrar_usuario_view import CadastrarUsuarioView
        view = CadastrarUsuarioView("aluno")
        self.centralizar_janela(view.root, 500, 400)
        view.start()

    def cadastrar_professor(self):
        from views.cadastrar_usuario_view import CadastrarUsuarioView
        view = CadastrarUsuarioView("professor")
        self.centralizar_janela(view.root, 500, 400)
        view.start()

    def cadastrar_disciplina(self):
        from views.cadastrar_disciplina_view import CadastrarDisciplinaView
        view = CadastrarDisciplinaView()
        self.centralizar_janela(view.root, 500, 400)
        view.start()

    def cadastrar_aluno_disciplina(self):
        from views.cadastrar_aluno_disciplina_view import CadastrarAlunoDisciplinaView
        view = CadastrarAlunoDisciplinaView()
        self.centralizar_janela(view.root, 500, 400)
        view.start()

    def start(self):
        self.root.mainloop()
