import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


class CadastrarDisciplinaView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cadastrar Disciplina")
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
        ttk.Label(main_frame, text="Cadastrar Disciplina", font=("Arial", 16, "bold"), style="TLabel").pack(pady=(0, 20))

        # Campo Nome da Disciplina
        ttk.Label(main_frame, text="Nome da Disciplina:", style="TLabel").pack(pady=5)
        self.entry_nome = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_nome.pack(pady=5)

        # Campo Descrição (opcional)
        ttk.Label(main_frame, text="Descrição (opcional):", style="TLabel").pack(pady=5)
        self.entry_descricao = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_descricao.pack(pady=5)

        # Campo Matrícula do Professor
        ttk.Label(main_frame, text="Matrícula do Professor:", style="TLabel").pack(pady=5)
        self.entry_matricula_professor = ttk.Entry(main_frame, style="TEntry", width=30)
        self.entry_matricula_professor.pack(pady=5)

        # Botão de Salvar
        ttk.Button(main_frame, text="Salvar", command=self.salvar, style="TButton").pack(pady=20)

    def log_debug(self, message):
        """
        Logs debug information to a file named 'debug.txt'.
        :param message: The message to log.
        """
        with open("debug.txt", "a") as debug_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            debug_file.write(f"[{timestamp}] {message}\n")

    def buscar_id_por_matricula(self, matricula):
        """
        Busca o ID do professor com base na matrícula.
        
        :param matricula: Número de matrícula do professor.
        :return: ID do professor ou None se não encontrado.
        """
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id FROM usuarios WHERE matricula=?
            ''', (matricula,))
            resultado = cursor.fetchone()
            conn.close()
            if resultado:
                return resultado[0]  # Retorna o ID do professor
            else:
                return None  # Retorna None se a matrícula não for encontrada
        except Exception as e:
            self.log_debug(f"Erro ao buscar ID por matrícula: {e}")
            return None

    def salvar(self):
        nome = self.entry_nome.get().strip()
        descricao = self.entry_descricao.get().strip()
        matricula_professor = self.entry_matricula_professor.get().strip()

        # Log inputs for debugging
        self.log_debug(f"Inputs recebidos - Nome: '{nome}', Descrição: '{descricao}', Matrícula do Professor: '{matricula_professor}'")

        if not nome or not matricula_professor:
            error_message = "Erro: Nome e matrícula do professor são obrigatórios."
            self.log_debug(error_message)
            messagebox.showerror("Erro", error_message)
            return

        try:
            # Buscar o ID do professor usando a matrícula
            professor_id = self.buscar_id_por_matricula(matricula_professor)
            if not professor_id:
                error_message = "Erro: Professor não encontrado com a matrícula fornecida."
                self.log_debug(error_message)
                messagebox.showerror("Erro", error_message)
                return

            # Conectar ao banco de dados e inserir a nova disciplina
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO disciplinas (nome, descricao, professor_id)
                VALUES (?, ?, ?)
            ''', (nome, descricao or "", professor_id))
            conn.commit()
            success_message = "Disciplina cadastrada com sucesso!"
            self.log_debug(success_message)
            messagebox.showinfo("Sucesso", success_message)
            self.root.destroy()
        except Exception as e:
            error_message = f"Erro ao salvar disciplina: {e}"
            self.log_debug(error_message)
            messagebox.showerror("Erro", error_message)
        finally:
            if 'conn' in locals():
                conn.close()
            self.log_debug("Conexão com o banco de dados fechada.")

    def start(self):
        self.root.mainloop()