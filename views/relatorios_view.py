# views/relatorio_view.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from models.relatorio_model import RelatorioModel
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


class RelatoriosView:
    def __init__(self, master=None):
        self.master = master
        self.model = RelatorioModel()

        # Criar janela principal
        self.root = tk.Toplevel(self.master) if self.master else tk.Tk()
        self.root.title("Relatório Geral")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        if self.master:
            self.root.transient(self.master)
            self.root.grab_set()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0056b3")])
        style.configure("TLabel", font=("Arial", 14), background="#f5f5f5")
        style.configure("Treeview", font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ttk.Label(main_frame, text="Relatórios do Sistema", font=("Arial", 16, "bold")).pack(pady=(0, 10))

        # Abas de relatórios
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)

        # Aba: Alunos por Disciplina
        aba_disciplina = ttk.Frame(notebook)
        notebook.add(aba_disciplina, text="Alunos por Turma")

        ttk.Label(aba_disciplina, text="Quantidade de Alunos por Disciplina", font=("Arial", 14)).pack(pady=10)

        self.tree_disciplina = ttk.Treeview(
            aba_disciplina,
            columns=("Disciplina", "Total de Alunos"),
            show="headings"
        )
        self.tree_disciplina.heading("Disciplina", text="Disciplina")
        self.tree_disciplina.heading("Total de Alunos", text="Total de Alunos")
        self.tree_disciplina.pack(fill="both", expand=True, padx=10, pady=10)

        btn_exportar_disciplina = ttk.Button(
            aba_disciplina,
            text="Exportar para CSV",
            command=self.exportar_alunos_por_disciplina
        )
        btn_exportar_disciplina.pack(pady=10)

        # Aba: Presença dos Alunos
        aba_presenca = ttk.Frame(notebook)
        notebook.add(aba_presenca, text="Presença dos Alunos")

        ttk.Label(aba_presenca, text="Porcentagem de Presença por Aluno", font=("Arial", 14)).pack(pady=10)

        self.tree_presenca = ttk.Treeview(
            aba_presenca,
            columns=("Aluno", "Disciplina", "Presença (%)"),
            show="headings"
        )
        self.tree_presenca.heading("Aluno", text="Aluno")
        self.tree_presenca.heading("Disciplina", text="Disciplina")
        self.tree_presenca.heading("Presença (%)", text="Presença (%)")
        self.tree_presenca.pack(fill="both", expand=True, padx=10, pady=10)

        btn_exportar_presenca = ttk.Button(
            aba_presenca,
            text="Exportar Presenças",
            command=self.exportar_presencas_alunos
        )
        btn_exportar_presenca.pack(pady=10)

        # Aba: Notas Médias
        aba_notas = ttk.Frame(notebook)
        notebook.add(aba_notas, text="Notas dos Alunos")

        ttk.Label(aba_notas, text="Média das Notas por Aluno", font=("Arial", 14)).pack(pady=10)

        self.tree_notas = ttk.Treeview(
            aba_notas,
            columns=("Aluno", "Disciplina", "Média"),
            show="headings"
        )
        self.tree_notas.heading("Aluno", text="Aluno")
        self.tree_notas.heading("Disciplina", text="Disciplina")
        self.tree_notas.heading("Média", text="Média")
        self.tree_notas.pack(fill="both", expand=True, padx=10, pady=10)

        btn_exportar_notas = ttk.Button(
            aba_notas,
            text="Exportar Notas",
            command=self.exportar_notas_alunos
        )
        btn_exportar_notas.pack(pady=10)

        # Aba: Gráficos
        aba_graficos = ttk.Frame(notebook)
        notebook.add(aba_graficos, text="Gráficos")

        ttk.Label(aba_graficos, text="Visualização Gráfica", font=("Arial", 14)).pack(pady=10)

        ttk.Button(aba_graficos, text="Gráfico de Alunos por Turma", command=self.grafico_alunos_por_turma).pack(pady=5)
        ttk.Button(aba_graficos, text="Gráfico de Presença dos Alunos", command=self.grafico_presenca_alunos).pack(pady=5)
        ttk.Button(aba_graficos, text="Gráfico de Notas Médias", command=self.grafico_notas_alunos).pack(pady=5)

        self.carregar_dados_iniciais()

    def carregar_dados_iniciais(self):
        """Carrega os dados nas Treeviews."""
        # Alunos por disciplina
        dados_disciplina = self.model.buscar_alunos_por_disciplina()
        for disciplina, total in dados_disciplina:
            self.tree_disciplina.insert("", "end", values=(disciplina, total))

        # Presença dos alunos
        dados_presenca = self.model.buscar_presencas_por_aluno()
        for aluno, disciplina, porcentagem in dados_presenca:
            self.tree_presenca.insert("", "end", values=(aluno, disciplina, porcentagem))

        # Notas dos alunos
        dados_notas = self.model.buscar_notas_medias()
        for aluno, disciplina, media in dados_notas:
            self.tree_notas.insert("", "end", values=(aluno, disciplina, media))

    def exportar_alunos_por_disciplina(self):
        dados = self.model.buscar_alunos_por_disciplina()
        sucesso = self.model.exportar_para_csv(
            [(d[0], d[1]) for d in dados],
            ["Disciplina", "Total de Alunos"],
            "relatorio_alunos_por_disciplina.csv"
        )
        if sucesso:
            messagebox.showinfo("Sucesso", "✅ Relatório salvo como 'relatorio_alunos_por_disciplina.csv'")
        else:
            messagebox.showerror("Erro", "❌ Falha ao salvar o relatório.")

    def exportar_presencas_alunos(self):
        dados = self.model.buscar_presencas_por_aluno()
        sucesso = self.model.exportar_para_csv(
            [(a, d, p) for a, d, p in dados],
            ["Aluno", "Disciplina", "Presença (%)"],
            "relatorio_presencas.csv"
        )
        if sucesso:
            messagebox.showinfo("Sucesso", "✅ Relatório salvo como 'relatorio_presencas.csv'")
        else:
            messagebox.showerror("Erro", "❌ Falha ao salvar o relatório.")

    def exportar_notas_alunos(self):
        dados = self.model.buscar_notas_medias()
        sucesso = self.model.exportar_para_csv(
            [(a, d, m) for a, d, m in dados],
            ["Aluno", "Disciplina", "Média"],
            "relatorio_notas.csv"
        )
        if sucesso:
            messagebox.showinfo("Sucesso", "✅ Relatório salvo como 'relatorio_notas.csv'")
        else:
            messagebox.showerror("Erro", "❌ Falha ao salvar o relatório.")

    def grafico_alunos_por_turma(self):
        dados = self.model.buscar_alunos_por_disciplina()
        if not dados:
            messagebox.showwarning("Dados Nulos", "Nenhum dado encontrado.")
            return

        disciplinas = [d[0] for d in dados]
        totais = [d[1] for d in dados]

        plt.figure(figsize=(10, 5))
        sns.barplot(x=totais, y=disciplinas, palette="viridis")
        plt.title("Quantidade de Alunos por Disciplina")
        plt.xlabel("Quantidade")
        plt.ylabel("Disciplina")
        plt.tight_layout()
        plt.show()

    def grafico_presenca_alunos(self):
        dados = self.model.buscar_presencas_por_aluno()
        if not dados:
            messagebox.showwarning("Dados Nulos", "Nenhum dado de presença encontrado.")
            return

        alunos = [d[0] for d in dados]
        presencas = [d[2] for d in dados]

        plt.figure(figsize=(10, 5))
        sns.histplot(presencas, bins=10, kde=True, color="green")
        plt.title("Distribuição de Frequência dos Alunos")
        plt.xlabel("Porcentagem de Presença (%)")
        plt.ylabel("Número de Alunos")
        plt.tight_layout()
        plt.show()

    def grafico_notas_alunos(self):
        dados = self.model.buscar_notas_medias()
        if not dados:
            messagebox.showwarning("Dados Nulos", "Nenhum dado de nota encontrado.")
            return

        medias = [d[2] for d in dados if d[2] is not None]

        if not medias:
            messagebox.showwarning("Sem Dados", "Não há notas para exibir no gráfico.")
            return

        plt.figure(figsize=(10, 5))
        plt.hist(medias, bins=10, color="skyblue", edgecolor="black")
        plt.axvline(sum(medias)/len(medias), color="red", linestyle="dashed", label="Média")
        plt.title("Distribuição das Notas dos Alunos")
        plt.xlabel("Nota")
        plt.ylabel("Frequência")
        plt.legend()
        plt.grid(True)
        plt.show()

    def start(self):
        self.root.mainloop()