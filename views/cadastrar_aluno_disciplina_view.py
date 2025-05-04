import tkinter as tk
from tkinter import ttk, messagebox
from models.aluno_disciplina import AlunoDisciplinaModel  
from datetime import datetime


class CadastrarAlunoDisciplinaView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cadastrar Aluno em Disciplina")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        # Instanciar model
        self.model = AlunoDisciplinaModel()

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
        ttk.Label(main_frame, text="Cadastrar Aluno em Disciplina", font=("Arial", 16, "bold"), style="TLabel").pack(pady=(0, 20))

        # Campo Matrícula do Aluno
        ttk.Label(main_frame, text="Matrícula do Aluno:", style="TLabel").pack(pady=5)
        self.entry_matricula_aluno = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_matricula_aluno.pack(pady=5)

        # Botão Buscar CPF
        ttk.Button(main_frame, text="Buscar CPF", command=self.buscar_cpf_por_matricula).pack(pady=10)

        # Campo CPF do Aluno (somente leitura)
        ttk.Label(main_frame, text="CPF do Aluno:", style="TLabel").pack(pady=5)
        self.entry_cpf_aluno = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_cpf_aluno.pack(pady=5)
        self.entry_cpf_aluno.config(state="readonly")

        # Seleção de disciplina
        ttk.Label(main_frame, text="Selecione a Disciplina:", style="TLabel").pack(pady=5)
        self.combo_disciplinas = ttk.Combobox(main_frame, state="readonly", width=30)
        self.combo_disciplinas.pack(pady=5)
        self.carregar_disciplinas()

        # Botão Cadastrar
        ttk.Button(main_frame, text="Cadastrar", command=self.cadastrar).pack(pady=20)

    def carregar_disciplinas(self):
        """Carrega as disciplinas no Combobox."""
        try:
            disciplinas = self.model.buscar_disciplinas()
            self.combo_disciplinas["values"] = disciplinas
            if disciplinas:
                self.combo_disciplinas.current(0)  # Seleciona a primeira disciplina
        except Exception as e:
            self.model.log_debug(f"Erro ao carregar disciplinas: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao carregar as disciplinas.")

    def buscar_cpf_por_matricula(self):
        """Busca o CPF do aluno pela matrícula."""
        matricula = self.entry_matricula_aluno.get().strip()
        if not matricula:
            messagebox.showwarning("Campo Obrigatório", "Preencha a matrícula do aluno.")
            return

        try:
            aluno = self.model.buscar_aluno_por_matricula(matricula)
            if not aluno:
                self.model.log_debug(f"Nenhum aluno encontrado com a matrícula: {matricula}")
                messagebox.showerror("Erro", "Aluno não encontrado.")
                return

            aluno_id, _, cpf = aluno
            self.entry_cpf_aluno.config(state="normal")
            self.entry_cpf_aluno.delete(0, tk.END)
            self.entry_cpf_aluno.insert(0, cpf)
            self.entry_cpf_aluno.config(state="readonly")

        except Exception as e:
            self.model.log_debug(f"Erro ao buscar CPF: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao buscar o CPF.")

    def cadastrar(self):
        """Cadastra o aluno na disciplina selecionada."""
        cpf_aluno = self.entry_cpf_aluno.get().strip()
        nome_disciplina = self.combo_disciplinas.get()
        if not cpf_aluno or not nome_disciplina:
            messagebox.showwarning("Campos Incompletos", "Por favor, preencha todos os campos.")
            return

        try:
            # Buscar aluno pelo CPF
            self.model.cursor.execute("SELECT id FROM usuarios WHERE cpf=?", (cpf_aluno,))
            aluno_id = self.model.cursor.fetchone()[0]
            if not aluno_id:
                raise ValueError("Aluno não encontrado.")

            # Buscar ID da disciplina
            disciplina_id = self.model.buscar_id_disciplina(nome_disciplina)
            if not disciplina_id:
                raise ValueError("Disciplina não encontrada.")

            # Verificar se aluno já está cadastrado
            if self.model.verificar_se_aluno_ja_matriculado(aluno_id, disciplina_id):
                messagebox.showerror("Erro", "O aluno já está matriculado nesta disciplina.")
                return

            # Realizar o cadastro
            sucesso = self.model.cadastrar_aluno_na_disciplina(aluno_id, disciplina_id)
            if sucesso:
                messagebox.showinfo("Sucesso", "✅ Aluno cadastrado com sucesso!")
                self.root.destroy()
            else:
                messagebox.showerror("Erro", "❌ Não foi possível cadastrar o aluno.")

        except Exception as e:
            self.model.log_debug(f"Erro ao cadastrar aluno: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro. Consulte os logs para mais detalhes.")

    def start(self):
        self.root.mainloop()