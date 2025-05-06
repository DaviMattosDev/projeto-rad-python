# views/remover_aluno_professor_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.remover_aluno_professor_model import RemoverAlunoProfessorModel
from datetime import datetime
import sqlite3


class RemoverAlunoProfessorView:
    def __init__(self, master=None):
        """
        Tela para remover aluno de uma disciplina, com base na matrícula.
        :param master: Janela pai (ex: Tk ou Toplevel)
        """
        self.master = master
        self.model = RemoverAlunoProfessorModel()

        # Criar janela secundária
        self.root = tk.Toplevel(self.master)
        self.root.title("Remover Aluno de Disciplina")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
        style.configure("TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0056b3")])
        style.configure("TFrame", background="#f5f5f5")

        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # === Campo Matrícula ===
        ttk.Label(main_frame, text="Matrícula do Aluno:", style="TLabel").pack(anchor="w")
        self.entry_matricula_aluno = ttk.Entry(main_frame, width=40)
        self.entry_matricula_aluno.pack(pady=5)
        self.entry_matricula_aluno.bind("<KeyRelease>", self.buscar_aluno_pela_matricula)

        # === Nome do Aluno (somente leitura) ===
        ttk.Label(main_frame, text="Nome do Aluno:", style="TLabel").pack(anchor="w")
        self.entry_nome_aluno = ttk.Entry(main_frame, width=40, state="readonly")
        self.entry_nome_aluno.pack(pady=5)

        # === Combobox Professor ===
        ttk.Label(main_frame, text="Selecione o Professor:", style="TLabel").pack(anchor="w")
        self.combo_professores = ttk.Combobox(main_frame, state="readonly", width=40)
        self.combo_professores.pack(pady=5)
        self.combo_professores.bind("<<ComboboxSelected>>", self.carregar_disciplinas_do_professor)

        # === Combobox Disciplinas ===
        ttk.Label(main_frame, text="Selecione a Disciplina:", style="TLabel").pack(anchor="w")
        self.combo_disciplinas = ttk.Combobox(main_frame, state="readonly", width=40)
        self.combo_disciplinas.pack(pady=5)
        self.combo_disciplinas.bind("<<ComboboxSelected>>", self.carregar_alunos_da_disciplina)

        # === Botão Remover Aluno ===
        self.btn_remover = ttk.Button(
            main_frame,
            text="Remover Aluno",
            command=self.confirmar_remocao
        )
        self.btn_remover.pack(pady=20)

        # === Dicionários auxiliares ===
        self.professor_dict = {}     # {nome_professor: id}
        self.disciplina_dict = {}   # {nome_disciplina: id}
        self.aluno_dict = {}       # {matricula: id_aluno}
        self.aluno_id_selecionado = None

        # Inicializa professores
        self.carregar_professores()

    def log_error(self, error_message):
        """Registra erros no arquivo debug.txt."""
        with open("debug.txt", "a") as log_file:
            log_file.write(f"[{datetime.now()}] {error_message}\n")

    def buscar_aluno_pela_matricula(self, event=None):
        """Busca o aluno pelo campo de matrícula."""
        try:
            matricula = self.entry_matricula_aluno.get().strip()
            if not matricula:
                self.entry_nome_aluno.config(state="normal")
                self.entry_nome_aluno.delete(0, tk.END)
                self.entry_nome_aluno.config(state="readonly")
                return

            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome_completo FROM usuarios WHERE matricula=?", (matricula,))
            aluno = cursor.fetchone()
            conn.close()

            if aluno:
                aluno_id, nome_completo = aluno
                self.entry_nome_aluno.config(state="normal")
                self.entry_nome_aluno.delete(0, tk.END)
                self.entry_nome_aluno.insert(0, nome_completo)
                self.entry_nome_aluno.config(state="readonly")
                self.aluno_id_selecionado = aluno_id
            else:
                self.log_error(f"Aluno com matrícula '{matricula}' não encontrado.")
                self.entry_nome_aluno.config(state="normal")
                self.entry_nome_aluno.delete(0, tk.END)
                self.entry_nome_aluno.config(state="readonly")
                self.aluno_id_selecionado = None
                messagebox.showwarning("Aluno Não Encontrado", f"Nenhum aluno encontrado com a matrícula '{matricula}'.")
        except Exception as e:
            self.log_error(f"Erro ao buscar aluno pela matrícula: {e}")
            messagebox.showerror("Erro", f"Ocorreu um erro ao buscar o aluno.")

    def carregar_professores(self):
        """Carrega professores no Combobox usando o modelo."""
        try:
            professores = self.model.buscar_professores()  # Retorna [(nome, id)]
            if not professores:
                raise ValueError("Nenhum professor encontrado.")
            self.professor_dict = {nome: id for nome, id in professores}
            self.combo_professores["values"] = list(self.professor_dict.keys())
        except Exception as e:
            self.log_error(f"Erro ao carregar professores: {e}")

    def carregar_disciplinas_do_professor(self, event=None):
        """Busca as disciplinas do professor selecionado usando o modelo."""
        try:
            professor_nome = self.combo_professores.get()
            if not professor_nome:
                return

            professor_id = self.professor_dict[professor_nome]

            # Buscar disciplinas via modelo
            disciplinas = self.model.buscar_disciplinas_do_professor(professor_id)
            if not disciplinas:
                self.combo_disciplinas.set("")
                self.combo_disciplinas["values"] = []
                return

            self.disciplina_dict = {nome: id for id, nome in disciplinas}
            self.combo_disciplinas["values"] = list(self.disciplina_dict.keys())
            self.combo_disciplinas.current(0)  # Seleciona a primeira por padrão
            self.carregar_alunos_da_disciplina()
        except Exception as e:
            self.log_error(f"Erro ao carregar disciplinas: {e}")

    def carregar_alunos_da_disciplina(self, event=None):
        """Carrega os alunos da disciplina selecionada usando o modelo."""
        try:
            disciplina_nome = self.combo_disciplinas.get()
            if not disciplina_nome:
                return

            disciplina_id = self.disciplina_dict[disciplina_nome]

            # Buscar alunos via modelo
            alunos = self.model.buscar_alunos_da_disciplina(disciplina_id)
            if not alunos:
                self.log_error(f"Nenhum aluno encontrado na disciplina ID {disciplina_id}.")
                self.btn_remover.config(state="disabled")
                return

            self.aluno_dict = {matricula: id for id, matricula in alunos}
            self.btn_remover.config(state="normal")  # Ativa o botão
        except Exception as e:
            self.log_error(f"Erro ao carregar alunos da disciplina: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar alunos.")

    def confirmar_remocao(self):
        """Confirma a remoção do aluno da disciplina."""
        try:
            matricula = self.entry_matricula_aluno.get().strip()
            aluno_id = self.aluno_id_selecionado
            professor_nome = self.combo_professores.get()
            disciplina_nome = self.combo_disciplinas.get()

            if not professor_nome or not disciplina_nome or not matricula:
                raise ValueError("Preencha todos os campos obrigatórios.")

            if not hasattr(self, 'aluno_id_selecionado') or self.aluno_id_selecionado is None:
                raise ValueError("Aluno inválido ou não encontrado.")

            if not hasattr(self, 'disciplina_dict') or disciplina_nome not in self.disciplina_dict:
                raise ValueError("Disciplina inválida.")

            professor_id = self.professor_dict[professor_nome]
            disciplina_id = self.disciplina_dict[disciplina_nome]
            aluno_id = self.aluno_id_selecionado

            # Pergunta confirmação
            confirmacao = messagebox.askyesno(
                "Confirmação",
                f"Tem certeza que deseja remover '{matricula}' da disciplina '{disciplina_nome}'?"
            )
            if not confirmacao:
                return

            sucesso = self.model.remover_aluno_de_professor(professor_id, aluno_id, disciplina_id)

            if sucesso:
                messagebox.showinfo("Sucesso", "✅ Aluno removido com sucesso.")
                self.entry_matricula_aluno.delete(0, tk.END)
                self.entry_nome_aluno.config(state="normal")
                self.entry_nome_aluno.delete(0, tk.END)
                self.entry_nome_aluno.config(state="readonly")
                self.carregar_alunos_da_disciplina()
            else:
                messagebox.showerror("Erro", "❌ Falha ao remover aluno.")
        except ValueError as ve:
            messagebox.showwarning("Aviso", str(ve))
        except Exception as e:
            self.log_error(f"Erro ao remover aluno da disciplina: {e}")
            messagebox.showerror("Erro", "Veja os logs para mais detalhes.")

    def start(self):
        """Inicia a interface gráfica da tela."""
        self.root.mainloop()