import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime

class ProfessorView:
    def __init__(self, usuario):
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title(f"Professor: {usuario.nome_completo}")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        # Configuração do estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
        style.configure("TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0056b3")])
        style.configure("TFrame", background="#f5f5f5")
        style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#ffffff")
        style.map("Treeview", background=[("selected", "#007bff")])
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # Abas
        self.tab_presenca = ttk.Frame(self.notebook, style="TFrame")
        self.tab_notas = ttk.Frame(self.notebook, style="TFrame")
        self.tab_avaliacoes = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.tab_presenca, text="Marcar Presença")
        self.notebook.add(self.tab_notas, text="Lançar Notas")
        self.notebook.add(self.tab_avaliacoes, text="Avaliações")

        # Carregar conteúdo das abas
        self.carregar_presencas()
        self.carregar_notas()
        self.carregar_avaliacoes()

    def buscar_alunos_do_professor(self):
        """Busca os alunos associados às disciplinas do professor."""
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT DISTINCT u.id, u.nome_completo 
        FROM usuarios u
        JOIN frequencias f ON u.id = f.aluno_id
        JOIN disciplinas d ON f.disciplina_id = d.id
        WHERE d.professor_id=?
        ''', (self.usuario.id,))
        alunos = cursor.fetchall()
        conn.close()
        return alunos

    def carregar_presencas(self):
        """Carrega a lista de presença dos alunos."""
        alunos = self.buscar_alunos_do_professor()
        ttk.Label(self.tab_presenca, text="Lista de Alunos - Hoje", font=("Arial", 14), style="TLabel").pack(pady=10)
        
        # Treeview para exibir a lista de presença
        self.tree_presenca = ttk.Treeview(
            self.tab_presenca,
            columns=("Nome", "Status"),
            show="headings",
            height=15
        )
        self.tree_presenca.heading("Nome", text="Nome do Aluno")
        self.tree_presenca.heading("Status", text="Status")
        self.tree_presenca.column("Nome", width=400)
        self.tree_presenca.column("Status", width=100)
        self.tree_presenca.pack(fill="both", expand=True)
        
        # Barra de rolagem
        scrollbar_presenca = ttk.Scrollbar(
            self.tab_presenca,
            orient="vertical",
            command=self.tree_presenca.yview
        )
        scrollbar_presenca.pack(side="right", fill="y")
        self.tree_presenca.configure(yscrollcommand=scrollbar_presenca.set)
        
        # Preencher a lista de presença
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        for aluno in alunos:
            aluno_id, aluno_nome = aluno
            presente = self.verificar_presenca(aluno_id, data_hoje)
            status = "Presente" if presente else "Ausente"
            cor = "green" if presente else "red"
            self.tree_presenca.insert("", "end", values=(aluno_nome, status), tags=(cor,))
        self.tree_presenca.tag_configure("red", foreground="red")
        self.tree_presenca.tag_configure("green", foreground="green")
        
        # Botões para confirmar presença e marcar falta
        ttk.Button(self.tab_presenca, text="Confirmar Presença", command=self.confirmar_presenca_individual).pack(pady=10)
        ttk.Button(self.tab_presenca, text="Marcar Falta", command=self.marcar_falta_individual).pack(pady=10)
    def confirmar_presenca_individual(self):
        """Confirma a presença de um aluno selecionado."""
        try:
            item_selecionado = self.tree_presenca.selection()[0]
            aluno_nome, _ = self.tree_presenca.item(item_selecionado, "values")
            aluno_info = next((aluno for aluno in self.buscar_alunos_do_professor() if aluno[1] == aluno_nome), None)
            if not aluno_info:
                raise ValueError("Aluno não encontrado.")
            aluno_id = aluno_info[0]
            data_aula = datetime.now().strftime("%Y-%m-%d")
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM frequencias WHERE aluno_id=? AND data_aula=?', (aluno_id, data_aula))
            row = cursor.fetchone()
            if row:
                cursor.execute('UPDATE frequencias SET presente=1 WHERE aluno_id=? AND data_aula=?', (aluno_id, data_aula))
            else:
                cursor.execute('''
                INSERT INTO frequencias (aluno_id, disciplina_id, data_aula, presente)
                VALUES (?, ?, ?, ?)
                ''', (aluno_id, 1, data_aula, True))
            conn.commit()
            conn.close()
            self.tree_presenca.item(item_selecionado, values=(aluno_nome, "Presente"), tags=("green",))
            messagebox.showinfo("Sucesso", f"Presença confirmada para {aluno_nome}!")
        except IndexError:
            messagebox.showwarning("Erro", "Selecione um aluno na lista.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao confirmar presença: {e}")

    def marcar_falta_individual(self):
        """Marca a falta de um aluno selecionado."""
        try:
            item_selecionado = self.tree_presenca.selection()[0]
            aluno_nome, _ = self.tree_presenca.item(item_selecionado, "values")
            aluno_info = next((aluno for aluno in self.buscar_alunos_do_professor() if aluno[1] == aluno_nome), None)
            if not aluno_info:
                raise ValueError("Aluno não encontrado.")
            aluno_id = aluno_info[0]
            data_aula = datetime.now().strftime("%Y-%m-%d")
            
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            
            # Verificar se já existe um registro de frequência para o aluno no dia
            cursor.execute('SELECT id FROM frequencias WHERE aluno_id=? AND data_aula=?', (aluno_id, data_aula))
            row = cursor.fetchone()
            
            if row:
                # Atualizar o registro existente para marcar falta
                cursor.execute('UPDATE frequencias SET presente=0 WHERE aluno_id=? AND data_aula=?', (aluno_id, data_aula))
            else:
                # Criar um novo registro de frequência com falta
                cursor.execute('''
                INSERT INTO frequencias (aluno_id, disciplina_id, data_aula, presente)
                VALUES (?, ?, ?, ?)
                ''', (aluno_id, 1, data_aula, False))  # Substitua `1` pelo ID da disciplina selecionada
            
            conn.commit()
            conn.close()
            
            # Atualizar a interface gráfica
            self.tree_presenca.item(item_selecionado, values=(aluno_nome, "Ausente"), tags=("red",))
            messagebox.showinfo("Sucesso", f"Falta registrada para {aluno_nome}!")
        
        except IndexError:
            messagebox.showwarning("Erro", "Selecione um aluno na lista.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao marcar falta: {e}")

    def carregar_notas(self):
        """Carrega a interface para lançar notas."""
        alunos = self.buscar_alunos_do_professor()
        ttk.Label(self.tab_notas, text="Lançar Notas", font=("Arial", 14), style="TLabel").pack(pady=10)

        # Combobox para selecionar aluno
        ttk.Label(self.tab_notas, text="Selecione um Aluno:", style="TLabel").pack(pady=5)
        self.combo_alunos_nota = ttk.Combobox(self.tab_notas, values=[a[1] for a in alunos], state="readonly")
        self.combo_alunos_nota.pack(pady=5)

        # Combobox para tipo de avaliação
        ttk.Label(self.tab_notas, text="Tipo de Avaliação:", style="TLabel").pack(pady=5)
        self.combo_tipo_avaliacao = ttk.Combobox(self.tab_notas, values=["AV1", "AV2", "AVS"], state="readonly")
        self.combo_tipo_avaliacao.pack(pady=5)

        # Entrada para nota
        ttk.Label(self.tab_notas, text="Nota (0.0 - 10.0):", style="TLabel").pack(pady=5)
        self.entry_nota = ttk.Entry(self.tab_notas)
        self.entry_nota.pack(pady=5)

        # Checkbox para falta
        self.check_faltou = tk.BooleanVar()
        ttk.Checkbutton(self.tab_notas, text="Marcar Falta", variable=self.check_faltou).pack(pady=5)

        # Botão para salvar nota
        ttk.Button(self.tab_notas, text="Salvar Nota", command=self.salvar_nota).pack(pady=10)

    def salvar_nota(self):
        """Salva a nota ou falta do aluno."""
        aluno_nome = self.combo_alunos_nota.get()
        tipo_avaliacao = self.combo_tipo_avaliacao.get()
        nota = self.entry_nota.get()
        faltou = self.check_faltou.get()
        if not aluno_nome or not tipo_avaliacao:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return
        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()
            # Buscar ID do aluno
            cursor.execute("SELECT id FROM usuarios WHERE nome_completo=?", (aluno_nome,))
            aluno_id = cursor.fetchone()[0]
            # Buscar ID da avaliação pelo tipo
            cursor.execute('''
            SELECT id FROM avaliacoes
            WHERE tipo_avaliacao=? AND disciplina_id=?
            ''', (tipo_avaliacao, 1))  # Substitua `1` pelo ID da disciplina selecionada
            avaliacao_id = cursor.fetchone()[0]
            # Salvar nota ou falta
            if faltou:
                cursor.execute('''
                INSERT INTO notas (aluno_id, disciplina_id, avaliacao_id, faltou)
                VALUES (?, ?, ?, ?)
                ''', (aluno_id, 1, avaliacao_id, True))
            else:
                nota = float(nota)
                if nota < 0 or nota > 10:
                    raise ValueError("Nota deve estar entre 0.0 e 10.0.")
                cursor.execute('''
                INSERT INTO notas (aluno_id, disciplina_id, avaliacao_id, valor_nota)
                VALUES (?, ?, ?, ?)
                ''', (aluno_id, 1, avaliacao_id, nota))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Nota/Falta salva para {aluno_nome}!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar nota: {e}")

    def buscar_disciplinas_do_professor(self):
        """Busca as disciplinas associadas ao professor."""
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT id, nome 
        FROM disciplinas 
        WHERE professor_id=?
        ''', (self.usuario.id,))
        disciplinas = cursor.fetchall()
        conn.close()
        return disciplinas        

    def carregar_avaliacoes(self):
        """Carrega a interface para criar avaliações."""
        disciplinas = self.buscar_disciplinas_do_professor()
        ttk.Label(self.tab_avaliacoes, text="Criar Avaliações", font=("Arial", 14), style="TLabel").pack(pady=10)
        
        # Combobox para selecionar disciplina
        if len(disciplinas) > 1:
            ttk.Label(self.tab_avaliacoes, text="Selecione a Disciplina:", style="TLabel").pack(pady=5)
            self.combo_disciplinas = ttk.Combobox(self.tab_avaliacoes, values=[d[1] for d in disciplinas], state="readonly")
            self.combo_disciplinas.pack(pady=5)
            self.disciplinas_dict = {d[1]: d[0] for d in disciplinas}
        elif len(disciplinas) == 1:
            self.disciplina_selecionada = disciplinas[0][0]
        else:
            messagebox.showwarning("Aviso", "Nenhuma disciplina encontrada para este professor.")
            return
        # Entrada para descrição da avaliação
        ttk.Label(self.tab_avaliacoes, text="Descrição da Avaliação:", style="TLabel").pack(pady=5)
        self.entry_descricao_avaliacao = ttk.Entry(self.tab_avaliacoes)
        self.entry_descricao_avaliacao.pack(pady=5)

        # Calendário para data da avaliação
        ttk.Label(self.tab_avaliacoes, text="Data da Avaliação:", style="TLabel").pack(pady=5)
        self.calendario = DateEntry(self.tab_avaliacoes, date_pattern="yyyy-mm-dd")
        self.calendario.pack(pady=5)

        # Combobox para tipo de avaliação
        ttk.Label(self.tab_avaliacoes, text="Tipo de Avaliação:", style="TLabel").pack(pady=5)
        self.combo_tipo_avaliacao = ttk.Combobox(self.tab_avaliacoes, values=["AV1", "AV2", "AVS"], state="readonly")
        self.combo_tipo_avaliacao.pack(pady=5)

        # Botão para criar avaliação
        ttk.Button(self.tab_avaliacoes, text="Criar Avaliação", command=self.criar_avaliacao).pack(pady=10)

        # Lista de avaliações criadas
        ttk.Label(self.tab_avaliacoes, text="Avaliações Criadas", font=("Arial", 14), style="TLabel").pack(pady=10)
        self.lista_avaliacoes = ttk.Treeview(
            self.tab_avaliacoes,
            columns=("Disciplina", "Data", "Descrição", "Tipo", "Aprovados", "Faltas"),
            show="headings",
            height=10
        )
        self.lista_avaliacoes.heading("Disciplina", text="Disciplina")
        self.lista_avaliacoes.heading("Data", text="Data")
        self.lista_avaliacoes.heading("Descrição", text="Descrição")
        self.lista_avaliacoes.heading("Tipo", text="Tipo")
        self.lista_avaliacoes.heading("Aprovados", text="Aprovados")
        self.lista_avaliacoes.heading("Faltas", text="Faltas")
        self.lista_avaliacoes.column("Disciplina", width=200)
        self.lista_avaliacoes.column("Data", width=100)
        self.lista_avaliacoes.column("Descrição", width=200)
        self.lista_avaliacoes.column("Tipo", width=100)
        self.lista_avaliacoes.column("Aprovados", width=100)
        self.lista_avaliacoes.column("Faltas", width=100)
        self.lista_avaliacoes.pack(fill="both", expand=True)

        # Barra de rolagem
        scrollbar_avaliacoes = ttk.Scrollbar(
            self.tab_avaliacoes,
            orient="vertical",
            command=self.lista_avaliacoes.yview
        )
        scrollbar_avaliacoes.pack(side="right", fill="y")
        self.lista_avaliacoes.configure(yscrollcommand=scrollbar_avaliacoes.set)

        # Carregar avaliações criadas
        self.carregar_avaliacoes_criadas()

    def criar_avaliacao(self):
        """Cria uma nova avaliação."""
        descricao = self.entry_descricao_avaliacao.get()
        tipo_avaliacao = self.combo_tipo_avaliacao.get()
        data_avaliacao = self.calendario.get_date().strftime("%Y-%m-%d")

        # Validate input fields
        if not descricao or not tipo_avaliacao:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        try:
            conn = sqlite3.connect("extensao.db")
            cursor = conn.cursor()

            # Determine the selected discipline ID
            if hasattr(self, "disciplina_selecionada"):
                disciplina_id = self.disciplina_selecionada
            else:
                nome_disciplina = self.combo_disciplinas.get()
                if not nome_disciplina:
                    messagebox.showwarning("Erro", "Selecione uma disciplina.")
                    return
                disciplina_id = self.disciplinas_dict[nome_disciplina]

            # Insert the new evaluation into the database
            cursor.execute('''
            INSERT INTO avaliacoes (disciplina_id, data_avaliacao, descricao, tipo_avaliacao)
            VALUES (?, ?, ?, ?)
            ''', (disciplina_id, data_avaliacao, descricao, tipo_avaliacao))

            conn.commit()
            conn.close()

            # Show success message
            messagebox.showinfo("Sucesso", "Avaliação criada com sucesso!")

            # Refresh the list of evaluations
            self.carregar_avaliacoes_criadas()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar avaliação: {e}")

    def carregar_avaliacoes_criadas(self):
        """Carrega as avaliações criadas pelo professor."""
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT a.id, d.nome, a.data_avaliacao, a.descricao, a.tipo_avaliacao
        FROM avaliacoes a
        JOIN disciplinas d ON a.disciplina_id = d.id
        WHERE d.professor_id=?
        ''', (self.usuario.id,))
        avaliacoes = cursor.fetchall()
        conn.close()
        self.lista_avaliacoes.delete(*self.lista_avaliacoes.get_children())
        data_atual = datetime.now().date()
        for avaliacao in avaliacoes:
            avaliacao_id, nome_disciplina, data_avaliacao, descricao, tipo_avaliacao = avaliacao
            data_avaliacao_date = datetime.strptime(data_avaliacao, "%Y-%m-%d").date()
            cor = "red" if data_avaliacao_date < data_atual else "black"
            # Contar alunos aprovados e faltas
            alunos_aprovados = self.contar_alunos_aprovados(avaliacao_id)
            faltas = self.contar_faltas(avaliacao_id)
            self.lista_avaliacoes.insert("", "end", values=(
                nome_disciplina, data_avaliacao, descricao, tipo_avaliacao, alunos_aprovados, faltas
            ), tags=(cor,))
        self.lista_avaliacoes.tag_configure("red", foreground="red")

    def contar_alunos_aprovados(self, avaliacao_id):
        """Conta o número de alunos aprovados em uma avaliação."""
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT COUNT(*) FROM notas
        WHERE avaliacao_id=? AND valor_nota >= 6
        ''', (avaliacao_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def contar_faltas(self, avaliacao_id):
        """Conta o número de faltas em uma avaliação."""
        conn = sqlite3.connect("extensao.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT COUNT(*) FROM notas
        WHERE avaliacao_id=? AND faltou=1
        ''', (avaliacao_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def start(self):
        """Inicia a interface gráfica."""
        self.root.mainloop()