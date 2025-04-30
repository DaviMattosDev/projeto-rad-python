import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Login - Sistema de Extensão")
        self.root.geometry("400x300")
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
        main_frame.pack(pady=40)

        # Título
        ttk.Label(main_frame, text="Login", font=("Arial", 18, "bold"), style="TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campo de Matrícula
        ttk.Label(main_frame, text="Matrícula:", style="TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_matricula = ttk.Entry(main_frame, style="TEntry")
        self.entry_matricula.grid(row=1, column=1, padx=10, pady=5)

        # Campo de Senha
        ttk.Label(main_frame, text="Senha:", style="TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_senha = ttk.Entry(main_frame, show="*", style="TEntry")
        self.entry_senha.grid(row=2, column=1, padx=10, pady=5)

        # Botão de Login
        self.btn_login = ttk.Button(main_frame, text="Entrar", command=self.controller.login, style="TButton")
        self.btn_login.grid(row=3, column=0, columnspan=2, pady=20)

    def get_dados_login(self):
        """Retorna os dados inseridos pelo usuário."""
        return self.entry_matricula.get(), self.entry_senha.get()

    def mostrar_erro(self, mensagem):
        """Exibe uma mensagem de erro em uma caixa de diálogo."""
        messagebox.showerror("Erro", mensagem)

    def start(self):
        """Inicia a interface gráfica."""
        self.root.mainloop()