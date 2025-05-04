import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from models.disciplina import DisciplinaModel  
from datetime import datetime


class CadastrarDisciplinaView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cadastrar Disciplina")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        # Instância do model
        self.model = DisciplinaModel()

        # Configuração do estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
        style.configure("TEntry", font=("Arial", 12), padding=5)
        style.configure("TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0056b3")])
        style.configure("TFrame", background="#f5f5f5")

        # Frame principal
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(padx=20, pady=20)

        # Título
        ttk.Label(main_frame, text="Cadastrar Disciplina", font=("Arial", 16, "bold"), style="TLabel").pack(pady=(0, 20))

        # Campo Nome da Disciplina
        ttk.Label(main_frame, text="Nome da Disciplina:", style="TLabel").pack(pady=5)
        self.entry_nome = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_nome.pack(pady=5)

        # Campo Descrição (opcional)
        ttk.Label(main_frame, text="Descrição (opcional):", style="TLabel").pack(pady=5)
        self.entry_descricao = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_descricao.pack(pady=5)

        # Campo Matrícula do Professor
        ttk.Label(main_frame, text="Matrícula do Professor:", style="TLabel").pack(pady=5)
        self.entry_matricula_professor = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_matricula_professor.pack(pady=5)

        # Botão Salvar
        ttk.Button(main_frame, text="Salvar", command=self.salvar).pack(pady=20)

    def salvar(self):
        """Salva a nova disciplina após validar os campos."""
        nome = self.entry_nome.get().strip()
        descricao = self.entry_descricao.get().strip()
        matricula = self.entry_matricula_professor.get().strip()

        # Log dos dados recebidos
        self.model.log_debug(f"Inputs - Nome: '{nome}', Descrição: '{descricao}', Matrícula do Professor: '{matricula}'")

        if not nome or not matricula:
            messagebox.showwarning("Campos Obrigatórios", "Nome e matrícula são obrigatórios.")
            return

        # Buscar professor pelo model
        professor_id = self.model.buscar_professor_por_matricula(matricula)
        if not professor_id:
            messagebox.showerror("Erro", "Professor não encontrado.")
            return

        # Cadastrar disciplina
        sucesso = self.model.cadastrar_disciplina(nome, descricao, professor_id)
        if sucesso:
            messagebox.showinfo("Sucesso", "Disciplina cadastrada com sucesso!")
            self.root.destroy()  # Fecha a janela após sucesso
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar a disciplina.")

    def start(self):
        self.root.mainloop()