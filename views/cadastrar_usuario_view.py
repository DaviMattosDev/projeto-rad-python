import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from models.usuario import Usuario
from utils.helpers import gerar_matricula, gerar_senha_padrao, hash_senha
import re

def validar_cpf(cpf):
    """Valida o formato do CPF."""
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    return len(cpf_limpo) == 11

def validar_email(email):
    """Valida o formato do email."""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

class CadastrarUsuarioView:
    def __init__(self, tipo_usuario):
        self.tipo = tipo_usuario
        self.root = tk.Tk()
        self.root.title(f"Cadastrar {tipo_usuario.capitalize()}")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

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
        ttk.Label(main_frame, text=f"Cadastrar {tipo_usuario.capitalize()}", font=("Arial", 16, "bold"), style="TLabel").pack(pady=(0, 20))

        # Campo Nome Completo
        ttk.Label(main_frame, text="Nome Completo:", style="TLabel").pack(pady=5)
        self.entry_nome = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_nome.pack(pady=5)

        # Campo Email
        ttk.Label(main_frame, text="Email:", style="TLabel").pack(pady=5)
        self.entry_email = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_email.pack(pady=5)

        # Campo CPF
        ttk.Label(main_frame, text="CPF (ex: 123.456.789-09):", style="TLabel").pack(pady=5)
        self.entry_cpf = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_cpf.pack(pady=5)

        # Campo Data de Nascimento
        ttk.Label(main_frame, text="Data de Nascimento:", style="TLabel").pack(pady=5)
        self.date_nascimento = DateEntry(
            main_frame,
            width=27,
            date_pattern="dd/mm/yyyy",
            background="darkblue",
            foreground="white"
        )
        self.date_nascimento.pack(pady=5)

        # Botão de Cadastro
        ttk.Button(main_frame, text="Cadastrar", command=self.cadastrar, style="TButton").pack(pady=20)

    def cadastrar(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        cpf = self.entry_cpf.get().strip()
        data_nascimento = self.date_nascimento.get_date().strftime("%d/%m/%Y")

        # Validações
        if not all([nome, email, cpf]):
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios.")
            return

        if not validar_cpf(cpf):
            messagebox.showwarning("Erro", "CPF inválido.")
            return

        if not validar_email(email):
            messagebox.showwarning("Erro", "Email inválido.")
            return

        try:
            matricula = gerar_matricula()
            senha_inicial = gerar_senha_padrao(data_nascimento, cpf)
            senha_hash = hash_senha(senha_inicial)

            # Gravar logs no arquivo debug.txt
            with open("debug.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"[DEBUG] Matrícula gerada: {matricula}\n")
                log_file.write(f"[DEBUG] Senha inicial (texto): {senha_inicial}\n")
                log_file.write(f"[DEBUG] Hash gerado: {senha_hash}\n")

            Usuario.cadastrar(nome, email, senha_hash, self.tipo, matricula, cpf, data_nascimento)

            messagebox.showinfo(
                "Sucesso",
                f"{self.tipo.capitalize()} cadastrado(a)!\n"
                f"Matrícula: {matricula}\n"
            )
            self.root.destroy()

        except Exception as e:
            with open("debug.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"[ERRO] Falha no cadastro: {e}\n")
            messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar: {e}")

    def start(self):
        self.root.mainloop()