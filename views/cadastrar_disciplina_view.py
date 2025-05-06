# views/cadastrar_disciplina_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.disciplina import DisciplinaModel
from datetime import datetime


class CadastrarDisciplinaView:
    def __init__(self, master=None):
        """
        Tela para cadastrar o professor em uma nova disciplina.
        """
        self.master = master
        self.model = DisciplinaModel()

        # Criar janela secundária
        self.root = tk.Toplevel(self.master)
        self.root.title("Cadastrar Disciplina")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        if self.master:
            self.root.transient(self.master)  # Janela filha
            self.root.grab_set()            # Bloqueia interação com a master até fechar essa janela

        # Centralizar sobre a janela principal
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (450 // 2)
        self.root.geometry(f"+{x}+{y}")

        # Configuração do estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
        style.configure("TEntry", font=("Arial", 12), padding=5)
        style.configure("TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0056b3")])
        style.configure("TFrame", background="#f5f5f5")

        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Título
        ttk.Label(main_frame, text="Cadastrar Disciplina", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # Carregar disciplinas existentes no Combobox
        try:
            disciplinas_existentes = self.model.buscar_todas_disciplinas()
            self.disciplinas_dict = {nome: id for nome, id in disciplinas_existentes}
        except Exception as e:
            self.disciplinas_dict = {}
            disciplinas_existentes = []

        ttk.Label(main_frame, text="Nome da Disciplina:", style="TLabel").pack(pady=5)
        self.combo_nome = ttk.Combobox(
            main_frame,
            values=[d[0] for d in disciplinas_existentes],
            state="normal"
        )
        self.combo_nome.pack(pady=5)

        # Campo Descrição
        ttk.Label(main_frame, text="Descrição (opcional):", style="TLabel").pack(pady=5)
        self.entry_descricao = ttk.Entry(main_frame, width=30)
        self.entry_descricao.pack(pady=5)

        # Campo Matrícula do Professor
        ttk.Label(main_frame, text="Matrícula do Professor:", style="TLabel").pack(pady=5)
        self.entry_matricula_professor = ttk.Entry(main_frame, width=30)
        self.entry_matricula_professor.pack(pady=5)
        self.entry_matricula_professor.bind("<KeyRelease>", self.atualizar_dados_professor)

        # Campo Nome do Professor (somente leitura)
        ttk.Label(main_frame, text="Nome do Professor:", style="TLabel").pack(pady=5)
        self.entry_nome_professor = ttk.Entry(main_frame, width=30, state="readonly")
        self.entry_nome_professor.pack(pady=5)

        # Campo Disciplina Antiga do Professor (se houver)
        ttk.Label(main_frame, text="Disciplina Atual do Professor:", style="TLabel").pack(pady=5)
        self.entry_disciplina_atual = ttk.Entry(main_frame, width=30, state="readonly")
        self.entry_disciplina_atual.pack(pady=5)

        # Botões
        btn_frame = ttk.Frame(main_frame, style="TFrame")
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Salvar",
            bg="#007bff",
            fg="white",
            font=("Arial", 12),
            padx=15,
            pady=5,
            command=self.salvar).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Cancelar",
            bg="#dc3545",
            fg="white",
            font=("Arial", 12),
            padx=15,
            pady=5,
            command=self.root.destroy
        ).pack(side="left", padx=10)


    def log_error(self, error_message):
        """Registra erros no arquivo debug.txt."""
        with open("debug.txt", "a") as log_file:
            log_file.write(f"[{datetime.now()}] {error_message}\n")

    def atualizar_dados_professor(self, event=None):
        """Atualiza nome do professor e disciplina ao digitar matrícula."""
        matricula = self.entry_matricula_professor.get().strip()
        if not matricula:
            self.entry_nome_professor.config(state="normal")
            self.entry_nome_professor.delete(0, tk.END)
            self.entry_nome_professor.config(state="readonly")
            self.entry_disciplina_atual.config(state="normal")
            self.entry_disciplina_atual.delete(0, tk.END)
            self.entry_disciplina_atual.config(state="readonly")
            return

        try:
            professor_info = self.model.buscar_professor_por_matricula(matricula)
            if not professor_info:
                raise ValueError("Professor não encontrado.")

            professor_id, nome_professor = professor_info
            self.entry_nome_professor.config(state="normal")
            self.entry_nome_professor.delete(0, tk.END)
            self.entry_nome_professor.insert(0, nome_professor)
            self.entry_nome_professor.config(state="readonly")

            disciplina_atual = self.model.buscar_disciplina_do_professor(professor_id)
            self.entry_disciplina_atual.config(state="normal")
            self.entry_disciplina_atual.delete(0, tk.END)
            if disciplina_atual:
                self.entry_disciplina_atual.insert(0, disciplina_atual[1])
            self.entry_disciplina_atual.config(state="readonly")
        except Exception as e:
            self.entry_nome_professor.config(state="normal")
            self.entry_nome_professor.delete(0, tk.END)
            self.entry_nome_professor.config(state="readonly")
            self.entry_disciplina_atual.config(state="normal")
            self.entry_disciplina_atual.delete(0, tk.END)
            self.entry_disciplina_atual.config(state="readonly")
            self.root.lift()
            self.root.focus_force()
            messagebox.showwarning("Aviso", f"Professor não encontrado.")
            self.log_error(f"Erro ao buscar dados do professor: {e}")
            self.root.lift()
            self.root.focus_force()

    def salvar(self):
        """Salva a nova disciplina após validar os campos."""
        try:
            nome = self.combo_nome.get().strip()
            descricao = self.entry_descricao.get().strip()
            matricula = self.entry_matricula_professor.get().strip()

            if not nome or not matricula:
                raise ValueError("Nome e matrícula são obrigatórios.")

            professor_info = self.model.buscar_professor_por_matricula(matricula)
            if not professor_info:
                raise ValueError("Professor não encontrado.")
            professor_id = professor_info[0]

            disciplina_atual = self.model.buscar_disciplina_do_professor(professor_id)
            if disciplina_atual:
                self.root.lift()
                self.root.focus_force()
                resposta = messagebox.askyesno(
                    "Professor já tem disciplina",
                    f"O professor já está ministrando '{disciplina_atual[1]}'.\n"
                    "Deseja remover ele dessa disciplina e adicionar nesta nova?",
                    parent=self.root
                )
                if not resposta:
                    self.root.lift()
                    self.root.focus_force()
                    return

            sucesso = self.model.cadastrar_disciplina(nome, descricao, professor_id)
            if sucesso:
                messagebox.showinfo("Sucesso", "✅ Disciplina cadastrada com sucesso.")
                self.root.after(500, self.root.destroy)
            else:
                raise Exception("Erro ao cadastrar disciplina.")
        except Exception as e:
            self.log_error(f"Erro ao salvar disciplina: {e}")
            self.root.lift()
            self.root.focus_force()
            messagebox.showerror("Erro", str(e))