import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario
from datetime import datetime
import re


class TrocarSenhaView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trocar Senha")
        self.root.geometry("500x400")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(False, False)

        # Centraliza a janela
        self.centralizar_janela(self.root, 500, 400)

        # Configuração do estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
        style.configure("TEntry", font=("Arial", 12))
        
        # Estilo personalizado para o botão
        style.configure("Custom.TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("Custom.TButton", background=[("active", "#0056b3"), ("pressed", "#004085")])

        # Frame principal
        frame = ttk.Frame(self.root, style="TFrame")
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Campo Matrícula ou CPF
        ttk.Label(frame, text="Matrícula ou CPF:", style="TLabel").pack(pady=5)
        self.entry_matricula = ttk.Entry(frame, width=30)
        self.entry_matricula.pack(pady=5)
        self.entry_matricula.bind("<KeyRelease>", lambda e: self.atualizar_informacoes_usuario())

        # Exibe informações do usuário (nome e tipo)
        self.info_usuario_frame = ttk.Frame(frame)
        self.info_usuario_frame.pack(pady=5)
        
        self.label_nome_usuario = ttk.Label(self.info_usuario_frame, text="", style="TLabel")
        self.label_tipo_usuario = ttk.Label(self.info_usuario_frame, text="", style="TLabel")
        self.label_nome_usuario.pack(anchor="w")
        self.label_tipo_usuario.pack(anchor="w")

        # Campo Nova Senha
        ttk.Label(frame, text="Nova Senha:", style="TLabel").pack(pady=5)
        self.entry_nova_senha = ttk.Entry(frame, show="*", width=30)
        self.entry_nova_senha.pack(pady=5)
        self.entry_nova_senha.bind("<KeyRelease>", lambda e: self.atualizar_cor_senha())

        # Campo Confirmar Nova Senha
        ttk.Label(frame, text="Confirmar Nova Senha:", style="TLabel").pack(pady=5)
        self.entry_confirma_senha = ttk.Entry(frame, show="*", width=30)
        self.entry_confirma_senha.pack(pady=5)
        self.entry_confirma_senha.bind("<KeyRelease>", lambda e: self.atualizar_cor_senha())

        # Label para força da senha
        self.forca_label = ttk.Label(frame, text="Força da senha: ", style="TLabel")
        self.forca_label.pack(pady=5)

        # Botão Salvar Senha - agora com estilo 'Custom.TButton' aplicado
        self.btn_salvar = ttk.Button(
            frame,
            text="Salvar Nova Senha",
            command=self.salvar_senha,
            style="Custom.TButton"  # ✅ Aplicando o estilo personalizado
        )
        self.btn_salvar.pack(pady=15)

        # Iniciar interface
        self.root.mainloop()

    def centralizar_janela(self, janela, largura, altura):
        screen_width = janela.winfo_screenwidth()
        screen_height = janela.winfo_screenheight()
        x = (screen_width // 2) - (largura // 2)
        y = (screen_height // 2) - (altura // 2)
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def atualizar_informacoes_usuario(self):
        matricula_ou_cpf = self.entry_matricula.get().strip()
        if not matricula_ou_cpf:
            self.label_nome_usuario.config(text="")
            self.label_tipo_usuario.config(text="")
            return

        try:
            usuario = Usuario.buscar_por_matricula(matricula_ou_cpf)
            if usuario:
                self.label_nome_usuario.config(text=f"Nome: {usuario.nome_completo}")
                self.label_tipo_usuario.config(text=f"Tipo: {usuario.tipo_usuario.capitalize()}")
            else:
                self.label_nome_usuario.config(text="Usuário não encontrado.")
                self.label_tipo_usuario.config(text="")
        except Exception as e:
            self.log_error(f"Erro ao buscar usuário para troca de senha: {e}")
            self.label_nome_usuario.config(text="")
            self.label_tipo_usuario.config(text="")

    def atualizar_cor_senha(self):
        senha = self.entry_nova_senha.get()
        confirma_senha = self.entry_confirma_senha.get()

        if not senha or not confirma_senha:
            self.forca_label.config(text="", foreground="black")
            return

        if senha != confirma_senha:
            self.forca_label.config(text="As senhas não coincidem.", foreground="red")
            return

        if len(senha) < 6:
            self.forca_label.config(text="Senha fraca 🔴", foreground="red")
        elif re.search(r"[A-Z]", senha) and re.search(r"[0-9]", senha) and \
             re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha) and len(senha) >= 8:
            self.forca_label.config(text="Senha forte 🟢", foreground="green")
        elif re.search(r"[A-Za-z]", senha) and re.search(r"[0-9]", senha) and len(senha) >= 6:
            self.forca_label.config(text="Senha média 🟡", foreground="orange")
        else:
            self.forca_label.config(text="Senha fraca 🔴", foreground="red")

    def salvar_senha(self):
        matricula_ou_cpf = self.entry_matricula.get().strip()
        nova_senha = self.entry_nova_senha.get().strip()
        confirma_senha = self.entry_confirma_senha.get().strip()

        if not matricula_ou_cpf:
            messagebox.showwarning("Campo Vazio", "Preencha a matrícula ou CPF.")
            return

        if not nova_senha or not confirma_senha:
            messagebox.showwarning("Campos Vazios", "Preencha todos os campos de senha.")
            return

        if nova_senha != confirma_senha:
            messagebox.showwarning("Senhas Diferentes", "As senhas digitadas não são iguais.")
            return

        if len(nova_senha) < 6:
            messagebox.showwarning("Senha Fraca", "A senha deve ter pelo menos 6 caracteres.")
            return

        sucesso = Usuario.trocar_senha(matricula_ou_cpf, nova_senha)
        if sucesso:
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
            self.root.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível alterar a senha.\nVeja o log para mais detalhes.")

    def log_error(self, error_message):
        with open("debug.txt", "a") as log_file:
            log_file.write(f"[{datetime.now()}] {error_message}\n")
