import tkinter as tk
from tkinter import ttk, messagebox
from models.aluno import Aluno  
from datetime import datetime
from views.trocar_senha_aluno_professor import TrocarSenhaAlunoProfessor  # Importa a tela de troca de senha


class AlunoView:
    def __init__(self, usuario):
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title(f"Aluno - {usuario.nome_completo}")
        self.root.geometry("950x750")  # Tela maior para visualização
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 14), background="#f5f5f5")
        style.configure("TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0056b3")])
        style.configure("TFrame", background="#f5f5f5")
        style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#ffffff")
        style.map("Treeview", background=[("selected", "#007bff")])
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Botões de Logout e Trocar Senha
        logout_frame = ttk.Frame(main_frame, style="TFrame")
        logout_frame.pack(anchor="ne", fill="x", pady=(0, 10))
        ttk.Button(logout_frame, text="Logout", command=self.logout).pack(side="right", padx=5)
        ttk.Button(
            logout_frame,
            text="Trocar Senha",
            command=self.abrir_troca_senha,
            style="TButton"
        ).pack(side="right", padx=5)

        # Disciplinas Cursadas
        disciplinas_label_frame = ttk.LabelFrame(main_frame, text="Disciplinas Cursadas", style="TFrame")
        disciplinas_label_frame.pack(fill="x", pady=(0, 15))

        self.tree_disciplinas = ttk.Treeview(
            disciplinas_label_frame,
            columns=("Disciplina", "Professor", "Frequência", "Nota"),
            show="headings",
            height=10
        )
        self.tree_disciplinas.heading("Disciplina", text="Disciplina")
        self.tree_disciplinas.heading("Professor", text="Professor")
        self.tree_disciplinas.heading("Frequência", text="Frequência")
        self.tree_disciplinas.heading("Nota", text="Nota Final")
        self.tree_disciplinas.column("Disciplina", width=300)
        self.tree_disciplinas.column("Professor", width=200)
        self.tree_disciplinas.column("Frequência", width=100)
        self.tree_disciplinas.column("Nota", width=100)
        self.tree_disciplinas.pack(side="left", fill="both", expand=True)

        scrollbar_disciplinas = ttk.Scrollbar(
            disciplinas_label_frame,
            orient="vertical",
            command=self.tree_disciplinas.yview
        )
        self.tree_disciplinas.configure(yscrollcommand=scrollbar_disciplinas.set)
        scrollbar_disciplinas.pack(side="right", fill="y")

        # Próximas Avaliações
        avaliacoes_label_frame = ttk.LabelFrame(main_frame, text="Próximas Avaliações", style="TFrame")
        avaliacoes_label_frame.pack(fill="x", pady=(0, 15))

        self.tree_avaliacoes = ttk.Treeview(
            avaliacoes_label_frame,
            columns=("Disciplina", "Data", "Descrição", "Tipo"),
            show="headings",
            height=5
        )
        self.tree_avaliacoes.heading("Disciplina", text="Disciplina")
        self.tree_avaliacoes.heading("Data", text="Data")
        self.tree_avaliacoes.heading("Descrição", text="Descrição")
        self.tree_avaliacoes.heading("Tipo", text="Tipo")
        self.tree_avaliacoes.column("Disciplina", width=300)
        self.tree_avaliacoes.column("Data", width=120)
        self.tree_avaliacoes.column("Descrição", width=300)
        self.tree_avaliacoes.column("Tipo", width=80)
        self.tree_avaliacoes.pack(side="left", fill="both", expand=True)

        scrollbar_avaliacoes = ttk.Scrollbar(
            avaliacoes_label_frame,
            orient="vertical",
            command=self.tree_avaliacoes.yview
        )
        self.tree_avaliacoes.configure(yscrollcommand=scrollbar_avaliacoes.set)
        scrollbar_avaliacoes.pack(side="right", fill="y")

        # Notas por Prova
        notas_label_frame = ttk.LabelFrame(main_frame, text="Notas por Prova", style="TFrame")
        notas_label_frame.pack(fill="x", pady=(0, 15))

        self.tree_notas = ttk.Treeview(
            notas_label_frame,
            columns=("Tipo", "Nota"),
            show="headings",
            height=5
        )
        self.tree_notas.heading("Tipo", text="Tipo de Avaliação")
        self.tree_notas.heading("Nota", text="Nota")
        self.tree_notas.column("Tipo", width=200)
        self.tree_notas.column("Nota", width=200)
        self.tree_notas.pack(side="left", fill="both", expand=True)

        scrollbar_notas = ttk.Scrollbar(
            notas_label_frame,
            orient="vertical",
            command=self.tree_notas.yview
        )
        self.tree_notas.configure(yscrollcommand=scrollbar_notas.set)
        scrollbar_notas.pack(side="right", fill="y")

        # Carrega os dados do aluno
        self.carregar_disciplinas()
        self.carregar_avaliacoes()
        self.carregar_notas()

    def log_error(self, error_message):
        """Registra erros no arquivo debug.txt."""
        with open("debug.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}: {error_message}\n")

    def carregar_disciplinas(self):
        """Carrega as disciplinas cursadas pelo aluno com frequência e nota."""
        try:
            disciplinas = Aluno.buscar_disciplinas(self.usuario.id)
            for nome, professor, disciplina_id in disciplinas:
                freq = Aluno.buscar_frequencia(self.usuario.id, disciplina_id)
                nota = Aluno.buscar_nota(self.usuario.id, disciplina_id)
                cor = "red" if freq < 50 else "black"
                self.tree_disciplinas.insert("", "end", values=(
                    nome,
                    professor,
                    f"{freq}%",
                    round(nota, 1) if nota is not None else "N/A"
                ), tags=(cor,))
            self.tree_disciplinas.tag_configure("red", foreground="red")
        except Exception as e:
            self.log_error(f"Erro ao carregar disciplinas: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro. Consulte os logs.")

    def carregar_avaliacoes(self):
        """Carrega apenas avaliações futuras."""
        try:
            avaliacoes = Aluno.buscar_avaliacoes(self.usuario.id)
            data_atual = datetime.now().date()
            for nome, data, descricao, tipo in avaliacoes:
                data_avaliacao = datetime.strptime(data, "%Y-%m-%d").date()
                if data_avaliacao >= data_atual:
                    self.tree_avaliacoes.insert("", "end", values=(nome, data, descricao, tipo))
        except Exception as e:
            self.log_error(f"Erro ao carregar avaliações: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao carregar as avaliações.")

    def carregar_notas(self):
        """Carrega as notas do aluno organizadas por tipo de avaliação (AV1, AV2, AVS)."""
        try:
            notas = Aluno.buscar_notas(self.usuario.id)
            for tipo, valor_nota in notas.items():
                self.tree_notas.insert("", "end", values=(tipo, valor_nota if valor_nota != "N/A" else "N/A"))
        except Exception as e:
            self.log_error(f"Erro ao carregar notas: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao carregar as notas.")

    def logout(self):
        """Fecha a janela atual e volta para a tela de login."""
        self.root.destroy()
        from controllers.auth_controller import AuthController
        auth = AuthController()
        auth.start()

    def abrir_troca_senha(self):
        """Abre a tela de troca de senha."""
        self.root.destroy()
        TrocarSenhaAlunoProfessor(usuario=self.usuario)

    def start(self):
        self.root.mainloop()