import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

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

        # Campo CPF do Aluno
        ttk.Label(main_frame, text="CPF do Aluno:", style="TLabel").pack(pady=5)
        self.entry_cpf_aluno = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_cpf_aluno.pack(pady=5)

        # Campo Nome da Disciplina
        ttk.Label(main_frame, text="Nome da Disciplina:", style="TLabel").pack(pady=5)
        self.entry_nome_disciplina = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_nome_disciplina.pack(pady=5)

        # Botão de Cadastro
        ttk.Button(main_frame, text="Cadastrar", command=self.cadastrar, style="TButton").pack(pady=20)

    def cadastrar(self):
        cpf_aluno = self.entry_cpf_aluno.get().strip()
        nome_disciplina = self.entry_nome_disciplina.get().strip()

        if not cpf_aluno or not nome_disciplina:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()

            # Buscar ID do aluno pelo CPF
            cursor.execute("SELECT id, nome_completo FROM usuarios WHERE cpf=?", (cpf_aluno,))
            aluno = cursor.fetchone()
            if not aluno:
                messagebox.showerror("Erro", "Aluno não encontrado.")
                return
            aluno_id, nome_aluno = aluno

            # Buscar ID da disciplina e professor responsável
            cursor.execute("""
            SELECT d.id, d.nome, u.nome_completo 
            FROM disciplinas d
            JOIN usuarios u ON d.professor_id = u.id
            WHERE d.nome=?
            """, (nome_disciplina,))
            disciplina = cursor.fetchone()
            if not disciplina:
                messagebox.showerror("Erro", "Disciplina não encontrada.")
                return
            disciplina_id, nome_disciplina, nome_professor = disciplina

            # Verificar se o aluno já está associado à disciplina
            cursor.execute("SELECT * FROM frequencias WHERE aluno_id=? AND disciplina_id=?", (aluno_id, disciplina_id))
            if cursor.fetchone():
                messagebox.showinfo("Aviso", "O aluno já está associado a esta disciplina.")
                return

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

            # Mostrar mensagem de sucesso com detalhes
            messagebox.showinfo(
                "Sucesso",
                f"✅ Aluno '{nome_aluno}' cadastrado na disciplina '{nome_disciplina}'!\n"
                f"Professor responsável: {nome_professor}"
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar aluno na disciplina: {e}")

        finally:
            conn.close()

    def start(self):
        self.root.mainloop()