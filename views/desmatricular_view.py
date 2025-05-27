from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox, ttk, StringVar
from models.desmatricular_model import DesmatricularModel


class DesmatricularUsuarioView:
    def __init__(self, master=None):
        self.model = DesmatricularModel()

        if master:
            self.root = Toplevel(master)
        else:
            self.root = Tk()

        self.root.title("Desmatricular Aluno/Professor")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        # Configuração dos estilos
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
        style.configure("TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0056b3")])
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TFrame", background="#f5f5f5")

        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Campo para matrícula ou CPF
        ttk.Label(main_frame, text="Matrícula ou CPF:", style="TLabel").pack(anchor="w", pady=5)
        self.entry_matricula = ttk.Entry(main_frame, width=40, style="TEntry")
        self.entry_matricula.pack(pady=5)

        # Botão de busca
        ttk.Button(
            main_frame,
            text="Buscar Usuário",
            command=self.buscar_usuario,
            style="TButton"
        ).pack(pady=10)

        # Nome do usuário encontrado
        self.label_nome = ttk.Label(main_frame, text="Nome: ", style="TLabel")
        self.label_nome.pack(anchor="w", pady=5)

        # Tipo do usuário (aluno/professor)
        self.label_tipo = ttk.Label(main_frame, text="Tipo: ", style="TLabel")
        self.label_tipo.pack(anchor="w", pady=5)

        # Botão de remoção (inicialmente desativado)
        self.btn_desmatricular = ttk.Button(
            main_frame,
            text="Desmatricular Usuário",
            command=self.desmatricular_usuario,
            style="TButton",
            state="disabled"
        )
        self.btn_desmatricular.pack(pady=20)

        # Botão limpar campos
        ttk.Button(
            main_frame,
            text="Limpar Campos",
            command=self.limpar_campos,
            style="TButton"
        ).pack(pady=10)

        # Centraliza e foca na janela
        self.centralizar_janela(self.root, 400, 300)
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def centralizar_janela(self, janela, largura, altura):
        x = (janela.winfo_screenwidth() - largura) // 2
        y = (janela.winfo_screenheight() - altura) // 2
        janela.geometry(f"{largura}x{altura}+{x}+{y}")
        janela.lift()
        janela.focus_force()

    def fechar_janela(self):
        """Fecha a janela e a conexão com o banco"""
        self.root.destroy()
        self.model.fechar_conexao()

    def buscar_usuario(self):
        matricula = self.entry_matricula.get().strip()
        if not matricula:
            messagebox.showwarning("Campo Vazio", "Por favor, insira uma matrícula ou CPF.")
            self.root.lift()
            self.root.focus_force()
            return

        usuario = self.model.buscar_por_matricula(matricula)
        if usuario:
            self.usuario_atual = usuario
            self.label_nome.config(text=f"Nome: {usuario['nome_completo']}")
            self.label_tipo.config(text=f"Tipo: {usuario['tipo_usuario'].capitalize()}")
            self.btn_desmatricular.config(state="normal")
        else:
            messagebox.showerror("Não Encontrado", "Usuário não encontrado.")
            self.root.lift()
            self.root.focus_force()
            self.limpar_campos()

    def desmatricular_usuario(self):
        confirmacao = messagebox.askyesno(
            "Confirmação",
            "Tem certeza que deseja desmatricular este usuário?\nEsta ação não pode ser desfeita."
        )
        if not confirmacao:
            self.root.lift()
            self.root.focus_force()
            return

        matricula = self.entry_matricula.get().strip()
        sucesso = self.model.desmatricular_usuario(matricula)
        if sucesso:
            messagebox.showinfo("Sucesso", "Usuário desmatriculado com sucesso!")
            self.root.lift()
            self.root.focus_force()
            self.limpar_campos()
        else:
            messagebox.showerror("Erro", "Falha ao desmatricular usuário.")
            self.root.lift()
            self.root.focus_force()

    def limpar_campos(self):
        self.entry_matricula.delete(0, "end")
        self.label_nome.config(text="Nome: ")
        self.label_tipo.config(text="Tipo: ")
        self.btn_desmatricular.config(state="disabled")

    def run(self):
        self.root.mainloop()

    def __del__(self):
        try:
            self.model.fechar_conexao()
        except:
            pass
