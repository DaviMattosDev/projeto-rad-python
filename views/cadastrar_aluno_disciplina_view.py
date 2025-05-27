import tkinter as tk
from tkinter import ttk, messagebox
from models.aluno_disciplina import AlunoDisciplinaModel  
from datetime import datetime


class CadastrarAlunoDisciplinaView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cadastrar Aluno em Disciplina")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        self.model = AlunoDisciplinaModel()

        # Estilo customizado para botões
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TButton",
                        font=("Arial", 12),
                        padding=10,
                        background="#007bff",
                        foreground="white")
        style.map("Custom.TButton",
                  background=[("active", "#0056b3")],
                  foreground=[("active", "white")])
        style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TFrame", background="#f5f5f5")

        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(padx=20, pady=20)

        ttk.Label(main_frame, text="Cadastrar Aluno em Disciplina", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        ttk.Label(main_frame, text="Matrícula do Aluno:", style="TLabel").pack(pady=5)
        self.entry_matricula_aluno = ttk.Entry(main_frame, width=30, style="TEntry")
        self.entry_matricula_aluno.pack(pady=5)

        ttk.Button(main_frame, text="Buscar CPF e Nome", command=self.buscar_dados_aluno, style="Custom.TButton").pack(pady=10)

        ttk.Label(main_frame, text="CPF do Aluno:", style="TLabel").pack(pady=5)
        self.entry_cpf_aluno = ttk.Entry(main_frame, width=30, state="readonly", style="TEntry")
        self.entry_cpf_aluno.pack(pady=5)

        ttk.Label(main_frame, text="Nome do Aluno:", style="TLabel").pack(pady=5)
        self.entry_nome_aluno = ttk.Entry(main_frame, width=30, state="readonly", style="TEntry")
        self.entry_nome_aluno.pack(pady=5)

        ttk.Label(main_frame, text="Selecione a Disciplina:", style="TLabel").pack(pady=5)
        self.combo_disciplinas = ttk.Combobox(main_frame, state="readonly", width=30, style="TEntry")
        self.combo_disciplinas.pack(pady=5)
        self.carregar_disciplinas()

        ttk.Button(main_frame, text="Cadastrar", command=self.cadastrar, style="Custom.TButton").pack(pady=20)

    def carregar_disciplinas(self):
        try:
            disciplinas = self.model.buscar_disciplinas()
            self.combo_disciplinas["values"] = disciplinas
            if disciplinas:
                self.combo_disciplinas.current(0)
        except Exception as e:
            self.model.log_debug(f"Erro ao carregar disciplinas: {e}")
            messagebox.showerror("Erro", "Falha ao carregar disciplinas.")
            self.root.lift()
            self.root.focus_force()

    def buscar_dados_aluno(self):
        matricula = self.entry_matricula_aluno.get().strip()
        if not matricula:
            messagebox.showwarning("Campo Obrigatório", "Preencha a matrícula do aluno.")
            self.root.lift()
            self.root.focus_force()
            return

        try:
            aluno = self.model.buscar_aluno_por_matricula(matricula)
            if not aluno:
                self.model.log_debug(f"Nenhum aluno encontrado com a matrícula: {matricula}")
                messagebox.showerror("Erro", "Aluno não encontrado.")
                self.limpar_campos_aluno()
                self.root.lift()
                self.root.focus_force()
                return

            aluno_id, nome, cpf = aluno
            self.entry_cpf_aluno.config(state="normal")
            self.entry_cpf_aluno.delete(0, tk.END)
            self.entry_cpf_aluno.insert(0, cpf)
            self.entry_cpf_aluno.config(state="readonly")

            self.entry_nome_aluno.config(state="normal")
            self.entry_nome_aluno.delete(0, tk.END)
            self.entry_nome_aluno.insert(0, nome)
            self.entry_nome_aluno.config(state="readonly")

        except Exception as e:
            self.model.log_debug(f"Erro ao buscar dados do aluno: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao buscar os dados do aluno.")
            self.root.lift()
            self.root.focus_force()

    def limpar_campos_aluno(self):
        self.entry_cpf_aluno.config(state="normal")
        self.entry_cpf_aluno.delete(0, tk.END)
        self.entry_cpf_aluno.config(state="readonly")

        self.entry_nome_aluno.config(state="normal")
        self.entry_nome_aluno.delete(0, tk.END)
        self.entry_nome_aluno.config(state="readonly")

    def cadastrar(self):
        cpf_aluno = self.entry_cpf_aluno.get().strip()
        nome_disciplina = self.combo_disciplinas.get()
        if not cpf_aluno or not nome_disciplina:
            messagebox.showwarning("Campos Incompletos", "Por favor, preencha todos os campos.")
            self.root.lift()
            self.root.focus_force()
            return

        try:
            confirmar = messagebox.askyesno(
                "Confirmação",
                f"Tem certeza que deseja cadastrar o aluno na disciplina '{nome_disciplina}'?"
            )
            self.root.lift()
            self.root.focus_force()
            if not confirmar:
                return

            self.model.cursor.execute("SELECT id FROM usuarios WHERE cpf=?", (cpf_aluno,))
            aluno_row = self.model.cursor.fetchone()
            if not aluno_row:
                raise ValueError("Aluno não encontrado pelo CPF.")
            aluno_id = aluno_row[0]

            disciplina_id = self.model.buscar_id_disciplina(nome_disciplina)
            if not disciplina_id:
                raise ValueError("Disciplina não encontrada.")

            if self.model.verificar_se_aluno_ja_matriculado(aluno_id, disciplina_id):
                messagebox.showerror("Erro", "O aluno já está matriculado nesta disciplina.")
                self.root.lift()
                self.root.focus_force()
                return

            sucesso = self.model.cadastrar_aluno_na_disciplina(aluno_id, disciplina_id)
            if sucesso:
                messagebox.showinfo("Sucesso", "✅ Aluno cadastrado com sucesso!")
                self.root.lift()
                self.root.focus_force()
                self.root.destroy()
            else:
                messagebox.showerror("Erro", "❌ Não foi possível cadastrar o aluno.")
                self.root.lift()
                self.root.focus_force()

        except Exception as e:
            self.model.log_debug(f"Erro ao cadastrar aluno na disciplina: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro. Consulte os logs para mais detalhes.")
            self.root.lift()
            self.root.focus_force()

    def start(self):
        self.root.mainloop()
