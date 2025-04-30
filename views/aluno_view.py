import tkinter as tk
from tkinter import ttk, messagebox
from models.aluno import Aluno  # Certifique-se de que o caminho está correto
from datetime import datetime

class AlunoView:
    def __init__(self, usuario):
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title(f"Aluno: {usuario.nome_completo}")
        self.centralizar_janela(self.root, 900, 700)  # Aumento no tamanho da tela
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        # Configuração do estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 14), background="#f5f5f5")
        style.configure("TFrame", background="#f5f5f5")
        style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#ffffff")
        style.map("Treeview", background=[("selected", "#007bff")])
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Frame principal
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título da seção de Disciplinas Cursadas
        ttk.Label(main_frame, text="Disciplinas Cursadas", style="TLabel").pack(pady=(0, 10))
        self.disciplinas_frame = ttk.Frame(main_frame, style="TFrame")
        self.disciplinas_frame.pack(fill="both", expand=True)

        # Treeview para exibir disciplinas cursadas
        self.tree_disciplinas = ttk.Treeview(
            self.disciplinas_frame,
            columns=("Disciplina", "Professor", "Frequência", "Nota"),
            show="headings",
            height=10
        )
        self.tree_disciplinas.heading("Disciplina", text="Disciplina")
        self.tree_disciplinas.heading("Professor", text="Professor")
        self.tree_disciplinas.heading("Frequência", text="Frequência")
        self.tree_disciplinas.heading("Nota", text="Nota")
        self.tree_disciplinas.column("Disciplina", width=300)
        self.tree_disciplinas.column("Professor", width=200)
        self.tree_disciplinas.column("Frequência", width=100)
        self.tree_disciplinas.column("Nota", width=100)
        self.tree_disciplinas.pack(side="left", fill="both", expand=True)

        # Barra de rolagem para disciplinas
        scrollbar_disciplinas = ttk.Scrollbar(
            self.disciplinas_frame,
            orient="vertical",
            command=self.tree_disciplinas.yview
        )
        scrollbar_disciplinas.pack(side="right", fill="y")
        self.tree_disciplinas.configure(yscrollcommand=scrollbar_disciplinas.set)

        # Título da seção de Próximas Avaliações
        ttk.Label(main_frame, text="Próximas Avaliações", style="TLabel").pack(pady=(20, 10))
        self.avaliacoes_frame = ttk.Frame(main_frame, style="TFrame")
        self.avaliacoes_frame.pack(fill="both", expand=True)

        # Treeview para exibir próximas avaliações
        self.tree_avaliacoes = ttk.Treeview(
            self.avaliacoes_frame,
            columns=("Disciplina", "Data", "Descrição", "Tipo"),
            show="headings",
            height=5
        )
        self.tree_avaliacoes.heading("Disciplina", text="Disciplina")
        self.tree_avaliacoes.heading("Data", text="Data")
        self.tree_avaliacoes.heading("Descrição", text="Descrição")
        self.tree_avaliacoes.heading("Tipo", text="Tipo")
        self.tree_avaliacoes.column("Disciplina", width=300)
        self.tree_avaliacoes.column("Data", width=150)
        self.tree_avaliacoes.column("Descrição", width=300)
        self.tree_avaliacoes.column("Tipo", width=100)
        self.tree_avaliacoes.pack(side="left", fill="both", expand=True)

        # Barra de rolagem para avaliações
        scrollbar_avaliacoes = ttk.Scrollbar(
            self.avaliacoes_frame,
            orient="vertical",
            command=self.tree_avaliacoes.yview
        )
        scrollbar_avaliacoes.pack(side="right", fill="y")
        self.tree_avaliacoes.configure(yscrollcommand=scrollbar_avaliacoes.set)

        # Título da seção de Notas por Tipo de Avaliação
        ttk.Label(main_frame, text="Notas por Tipo de Avaliação", style="TLabel").pack(pady=(20, 10))
        self.notas_frame = ttk.Frame(main_frame, style="TFrame")
        self.notas_frame.pack(fill="both", expand=True)

        # Treeview para exibir notas por tipo de avaliação
        self.tree_notas = ttk.Treeview(
            self.notas_frame,
            columns=("Tipo", "Nota"),
            show="headings",
            height=5
        )
        self.tree_notas.heading("Tipo", text="Tipo de Avaliação")
        self.tree_notas.heading("Nota", text="Nota")
        self.tree_notas.column("Tipo", width=200)
        self.tree_notas.column("Nota", width=200)
        self.tree_notas.pack(side="left", fill="both", expand=True)

        # Barra de rolagem para notas
        scrollbar_notas = ttk.Scrollbar(
            self.notas_frame,
            orient="vertical",
            command=self.tree_notas.yview
        )
        scrollbar_notas.pack(side="right", fill="y")
        self.tree_notas.configure(yscrollcommand=scrollbar_notas.set)

        # Carregar conteúdo
        self.carregar_disciplinas()
        self.carregar_avaliacoes()
        self.carregar_notas()

    def log_error(self, error_message):
        """Registra erros no arquivo debug.txt."""
        with open("debug.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}: {error_message}\n")

    def centralizar_janela(self, janela, largura, altura):
        """Centraliza uma janela na tela."""
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2
        janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def carregar_disciplinas(self):
        """Carrega as disciplinas cursadas pelo aluno com notas e frequência."""
        try:
            disciplinas = Aluno.buscar_disciplinas(self.usuario.id)
            for nome, professor, disciplina_id in disciplinas:
                freq = Aluno.buscar_frequencia(self.usuario.id, disciplina_id)
                nota = Aluno.buscar_nota(self.usuario.id, disciplina_id)
                cor = "red" if freq < 50 else "black"
                self.tree_disciplinas.insert("", "end", values=(nome, professor, f"{freq}%", nota if nota is not None else "N/A"), tags=(cor,))
            self.tree_disciplinas.tag_configure("red", foreground="red")
        except Exception as e:
            self.log_error(f"Erro ao carregar disciplinas: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao carregar as disciplinas. Consulte os logs para mais detalhes.")

    def carregar_avaliacoes(self):
        """Carrega as próximas avaliações do aluno filtrando por data."""
        try:
            avaliacoes = Aluno.buscar_avaliacoes(self.usuario.id)
            data_atual = datetime.now().date()
            for nome, data, descricao, tipo in avaliacoes:
                data_avaliacao = datetime.strptime(data, "%Y-%m-%d").date()
                if data_avaliacao >= data_atual:  # Filtra avaliações futuras ou atuais
                    self.tree_avaliacoes.insert("", "end", values=(nome, data, descricao, tipo))
        except Exception as e:
            self.log_error(f"Erro ao carregar avaliações: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao carregar as avaliações. Consulte os logs para mais detalhes.")

    def carregar_notas(self):
        """Carrega as notas do aluno organizadas por tipo de avaliação."""
        try:
            notas = Aluno.buscar_notas(self.usuario.id)
            for tipo, valor_nota in notas.items():
                self.tree_notas.insert("", "end", values=(tipo, valor_nota if valor_nota != "N/A" else "N/A"))
        except Exception as e:
            self.log_error(f"Erro ao carregar notas: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao carregar as notas. Consulte os logs para mais detalhes.")

    def start(self):
        """Inicia a interface gráfica."""
        self.root.mainloop()
