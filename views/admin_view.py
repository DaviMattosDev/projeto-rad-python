import tkinter as tk
from tkinter import ttk
from views.cadastrar_usuario_view import CadastrarUsuarioView
from views.cadastrar_disciplina_view import CadastrarDisciplinaView
from views.cadastrar_aluno_disciplina_view import CadastrarAlunoDisciplinaView

class AdminView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Administração")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

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

    def cadastrar_aluno(self):
        from views.cadastrar_usuario_view import CadastrarUsuarioView
        CadastrarUsuarioView("aluno").start()

    def cadastrar_professor(self):
        from views.cadastrar_usuario_view import CadastrarUsuarioView
        CadastrarUsuarioView("professor").start()

    def cadastrar_disciplina(self):
        from views.cadastrar_disciplina_view import CadastrarDisciplinaView
        CadastrarDisciplinaView().start()

    def cadastrar_aluno_disciplina(self):
        from views.cadastrar_aluno_disciplina_view import CadastrarAlunoDisciplinaView
        CadastrarAlunoDisciplinaView().start()

    def start(self):
        self.root.mainloop()