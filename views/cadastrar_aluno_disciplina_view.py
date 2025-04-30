import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class CadastrarAlunoDisciplinaView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cadastrar Aluno em Disciplina")
        self.root.geometry("500x400")
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
        ttk.Label(main_frame, text="Cadastrar Aluno em Disciplina", font=("Arial", 16, "bold"), style="TLabel").pack(pady=(0, 20))

        # Campo Matrícula do Aluno
        ttk.Label(main_frame, text="Matrícula do Aluno:", style="TLabel").pack(pady=5)
        self.entry_matricula_aluno = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_matricula_aluno.pack(pady=5)

        # Botão para buscar CPF pelo número de matrícula
        ttk.Button(main_frame, text="Buscar CPF", command=self.buscar_cpf_por_matricula, style="TButton").pack(pady=10)

        # Campo CPF do Aluno (será preenchido automaticamente após a busca)
        ttk.Label(main_frame, text="CPF do Aluno:", style="TLabel").pack(pady=5)
        self.entry_cpf_aluno = ttk.Entry(main_frame, style="TEntry", width=30, state="readonly")
        self.entry_cpf_aluno.pack(pady=5)

        # Combobox para selecionar disciplina
        ttk.Label(main_frame, text="Selecione a Disciplina:", style="TLabel").pack(pady=5)
        self.combo_disciplinas = ttk.Combobox(main_frame, style="TCombobox", state="readonly", width=30)
        self.combo_disciplinas.pack(pady=5)
        self.carregar_disciplinas()

        # Botão de Cadastro
        ttk.Button(main_frame, text="Cadastrar", command=self.cadastrar, style="TButton").pack(pady=20)

    def carregar_disciplinas(self):
        """Carrega as disciplinas disponíveis no Combobox."""
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()

            # Buscar todas as disciplinas disponíveis
            cursor.execute("SELECT nome FROM disciplinas")
            disciplinas = [row[0] for row in cursor.fetchall()]
            conn.close()

            # Preencher o Combobox com as disciplinas
            self.combo_disciplinas["values"] = disciplinas
            if disciplinas:
                self.combo_disciplinas.current(0)  # Seleciona a primeira disciplina por padrão

        except Exception as e:
            self.log_debug(f"Erro ao carregar disciplinas: {e}")

    def buscar_cpf_por_matricula(self):
        """Busca o CPF do aluno com base na matrícula."""
        matricula = self.entry_matricula_aluno.get().strip()

        if not matricula:
            self.log_debug("Informe a matrícula do aluno.")
            return

        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()

            # Buscar CPF do aluno pelo número de matrícula
            cursor.execute("SELECT cpf FROM usuarios WHERE matricula=?", (matricula,))
            aluno = cursor.fetchone()

            if not aluno:
                self.log_debug(f"Nenhum aluno encontrado com a matrícula: {matricula}")
                return

            cpf_aluno = aluno[0]

            # Preencher o campo de CPF automaticamente
            self.entry_cpf_aluno.config(state="normal")
            self.entry_cpf_aluno.delete(0, tk.END)
            self.entry_cpf_aluno.insert(0, cpf_aluno)
            self.entry_cpf_aluno.config(state="readonly")

        except Exception as e:
            self.log_debug(f"Erro ao buscar CPF: {e}")

        finally:
            conn.close()

    def cadastrar(self):
        """Cadastra o aluno na disciplina selecionada."""
        cpf_aluno = self.entry_cpf_aluno.get().strip()
        nome_disciplina = self.combo_disciplinas.get()

        if not cpf_aluno or not nome_disciplina:
            self.log_debug("Preencha todos os campos.")
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()

            # Buscar ID do aluno pelo CPF
            cursor.execute("SELECT id, nome_completo FROM usuarios WHERE cpf=?", (cpf_aluno,))
            aluno = cursor.fetchone()
            if not aluno:
                raise ValueError("Aluno não encontrado.")
            aluno_id, nome_aluno = aluno

            # Buscar ID da disciplina
            cursor.execute("SELECT id FROM disciplinas WHERE nome=?", (nome_disciplina,))
            disciplina = cursor.fetchone()
            if not disciplina:
                raise ValueError("Disciplina não encontrada.")
            disciplina_id = disciplina[0]

            # Verificar se o aluno já está associado à disciplina
            cursor.execute("SELECT * FROM frequencias WHERE aluno_id=? AND disciplina_id=?", (aluno_id, disciplina_id))
            if cursor.fetchone():
                raise ValueError("O aluno já está associado a esta disciplina.")

            # Inserir na tabela de frequências
            cursor.execute('''
            INSERT INTO frequencias (aluno_id, disciplina_id, data_aula, presente)
            VALUES (?, ?, ?, ?)
            ''', (aluno_id, disciplina_id, "2025-06-10", 1))

            # Inserir na tabela de notas (opcional)
            cursor.execute('''
            INSERT INTO notas (aluno_id, disciplina_id, valor_nota)
            VALUES (?, ?, ?)
            ''', (aluno_id, disciplina_id, None))

            conn.commit()

            # Exibir mensagem de sucesso
            messagebox.showinfo("Sucesso", f"✅ Aluno '{nome_aluno}' cadastrado na disciplina '{nome_disciplina}'!")

        except Exception as e:
            # Registrar o erro no debug.txt
            self.log_debug(f"Erro ao cadastrar aluno na disciplina: {e}")
            # Exibir mensagem genérica de erro para o usuário
            messagebox.showerror("Erro", "Ocorreu um erro ao cadastrar o aluno. Consulte o log para mais detalhes.")

        finally:
            conn.close()

    def log_debug(self, mensagem):
        """Grava logs no arquivo debug.txt."""
        with open("debug.txt", "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{timestamp}] {mensagem}\n")

    def start(self):
        self.root.mainloop()
