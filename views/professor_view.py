import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from models.professor import ProfessorModel
from datetime import datetime
from views.trocar_senha_aluno_professor import TrocarSenhaAlunoProfessor


class ProfessorView:
    def __init__(self, usuario):
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title(f"Professor: {usuario.nome_completo}")
        self.root.geometry("950x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        # Instanciar model
        self.model = ProfessorModel(usuario.id)
        self.model.atualizar_disciplinas_e_avaliacoes() 

        # Configuração do estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 14), background="#f5f5f5")
        style.configure("TButton", font=("Arial", 12), padding=10, background="#007bff", foreground="white")
        style.map("TButton", background=[("active", "#0056b3")])
        style.configure("TFrame", background="#f5f5f5")
        style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#ffffff")
        style.map("Treeview", background=[("selected", "#007bff")])
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Frame principal
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # === Canto superior direito logout ===
        logout_frame = ttk.Frame(main_frame, style="TFrame")
        logout_frame.pack(anchor="ne", fill="x", pady=(0, 10))
        ttk.Button(logout_frame, text="Logout", command=self.logout).pack(side="right")
        ttk.Button(logout_frame,text="Trocar Senha",command=self.abrir_troca_senha,style="TButton").pack(side="right", padx=5)

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

        # Carregar conteúdo
        try:
            self.carregar_presencas()
            self.carregar_notas()
            self.carregar_avaliacoes()
        except Exception as e:
            self.log_error(f"Erro ao inicializar interface: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao carregar a interface.")

    def log_error(self, error_message):
        """Registra erros no arquivo debug.txt."""
        with open("debug.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}: {error_message}\n")

    def logout(self):
        """Fecha a janela atual e volta para a tela de login."""
        self.root.destroy()
        from controllers.auth_controller import AuthController
        auth = AuthController()
        auth.start()

    def carregar_presencas(self):
        """Carrega a lista de presença dos alunos."""
        try:
            alunos = self.model.buscar_alunos_do_professor()
            ttk.Label(self.tab_presenca, text="Lista de Alunos - Hoje", font=("Arial", 14), style="TLabel").pack(pady=10)

            # Frame para Treeview + Scrollbar
            frame_lista = ttk.Frame(self.tab_presenca)
            frame_lista.pack(fill="both", expand=True)

            self.tree_presenca = ttk.Treeview(
                frame_lista,
                columns=("Nome", "Status"),
                show="headings",
                height=15
            )
            self.tree_presenca.heading("Nome", text="Nome do Aluno")
            self.tree_presenca.heading("Status", text="Status")
            self.tree_presenca.column("Nome", width=400)
            self.tree_presenca.column("Status", width=100)
            self.tree_presenca.pack(side="left", fill="both", expand=True)

            # Barra de rolagem
            scrollbar_presenca = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree_presenca.yview)
            self.tree_presenca.configure(yscrollcommand=scrollbar_presenca.set)
            scrollbar_presenca.pack(side="right", fill="y")

            # Preencher lista de alunos
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            for aluno in alunos:
                aluno_id, aluno_nome = aluno
                presente = self.model.verificar_presenca(aluno_id, data_hoje)
                status = "Presente" if presente else "Ausente"
                cor = "green" if presente else "red"
                self.tree_presenca.insert("", "end", values=(aluno_nome, status), tags=(cor,))
            self.tree_presenca.tag_configure("red", foreground="red")
            self.tree_presenca.tag_configure("green", foreground="green")

            # Botões
            ttk.Button(self.tab_presenca, text="Confirmar Presença", command=self.confirmar_presenca_individual).pack(pady=10)
            ttk.Button(self.tab_presenca, text="Marcar Falta", command=self.marcar_falta_individual).pack(pady=10)

        except Exception as e:
            self.log_error(f"Erro ao carregar presenças: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao carregar a aba de presença. Consulte os logs.")

    def confirmar_presenca_individual(self):
        """Confirma a presença de um aluno selecionado."""
        try:
            item_selecionado = self.tree_presenca.selection()[0]
            aluno_nome, _ = self.tree_presenca.item(item_selecionado, "values")
            aluno_info = next((aluno for aluno in self.model.alunos if aluno[1] == aluno_nome), None)
            if not aluno_info:
                raise ValueError("Aluno não encontrado.")
            aluno_id = aluno_info[0]
            data_aula = datetime.now().strftime("%Y-%m-%d")
            self.model.registrar_presenca(aluno_id, data_aula, True)
            self.tree_presenca.item(item_selecionado, values=(aluno_nome, "Presente"), tags=("green",))
            messagebox.showinfo("Sucesso", "Presença confirmada com sucesso!")
        except IndexError:
            messagebox.showwarning("Erro", "Selecione um aluno na lista.")
        except Exception as e:
            self.log_error(f"Erro ao confirmar presença: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao confirmar a presença. Consulte os logs.")

    def abrir_troca_senha(self):
        """Abre a tela de troca de senha."""
        self.root.destroy()
        TrocarSenhaAlunoProfessor(usuario=self.usuario)

    def marcar_falta_individual(self):
        """Marca a falta de um aluno selecionado."""
        try:
            item_selecionado = self.tree_presenca.selection()[0]
            aluno_nome, _ = self.tree_presenca.item(item_selecionado, "values")
            aluno_info = next((aluno for aluno in self.model.alunos if aluno[1] == aluno_nome), None)
            if not aluno_info:
                raise ValueError("Aluno não encontrado.")
            aluno_id = aluno_info[0]
            data_aula = datetime.now().strftime("%Y-%m-%d")
            self.model.registrar_presenca(aluno_id, data_aula, False)
            self.tree_presenca.item(item_selecionado, values=(aluno_nome, "Ausente"), tags=("red",))
            messagebox.showinfo("Sucesso", "Falta registrada com sucesso!")
        except IndexError:
            messagebox.showwarning("Erro", "Selecione um aluno na lista.")
        except Exception as e:
            self.log_error(f"Erro ao marcar falta: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao marcar a falta. Consulte os logs.")

    def carregar_notas(self):
        """Carrega a interface para lançar notas."""
        try:
            ttk.Label(self.tab_notas, text="Lançar Notas", font=("Arial", 14), style="TLabel").pack(pady=10)

            # Combobox Aluno
            ttk.Label(self.tab_notas, text="Selecione um Aluno:", style="TLabel").pack(pady=5)
            self.combo_alunos_nota = ttk.Combobox(self.tab_notas, values=[a[1] for a in self.model.alunos], state="readonly")
            self.combo_alunos_nota.pack(pady=5)

            # Combobox Tipo de Avaliação
            ttk.Label(self.tab_notas, text="Tipo de Avaliação:", style="TLabel").pack(pady=5)
            self.combo_tipo_avaliacao = ttk.Combobox(self.tab_notas, values=["AV1", "AV2", "AVS"], state="readonly")
            self.combo_tipo_avaliacao.pack(pady=5)

            # Entrada de nota
            ttk.Label(self.tab_notas, text="Nota (0.0 - 10.0):", style="TLabel").pack(pady=5)
            self.entry_nota = ttk.Entry(self.tab_notas)
            self.entry_nota.pack(pady=5)

            # Checkbox Marcar Falta
            self.check_faltou = tk.BooleanVar()
            ttk.Checkbutton(self.tab_notas, text="Marcar Falta", variable=self.check_faltou).pack(pady=5)

            # Botão salvar
            ttk.Button(self.tab_notas, text="Salvar Nota", command=self.salvar_nota).pack(pady=10)

        except Exception as e:
            self.log_error(f"Erro ao carregar notas: {e}")
            messagebox.showerror("Erro", "Ocorreu um problema ao carregar a aba de notas. Consulte os logs.")

    def salvar_nota(self):
        """Salva a nota ou falta do aluno."""
        try:
            aluno_nome = self.combo_alunos_nota.get()
            tipo_avaliacao = self.combo_tipo_avaliacao.get()
            faltou = self.check_faltou.get()
            aluno_info = next((aluno for aluno in self.model.alunos if aluno[1] == aluno_nome), None)
            avaliacao_info = self.model.buscar_avaliacao(tipo_avaliacao)

            if not aluno_info or not avaliacao_info:
                raise ValueError("Dados inválidos.")

            aluno_id, avaliacao_id = aluno_info[0], avaliacao_info[0]
            nota = float(self.entry_nota.get()) if not faltou and self.entry_nota.get() else None

            if faltou:
                self.model.salvar_nota(aluno_id, avaliacao_id, faltou=True)
            else:
                if not (0.0 <= nota <= 10.0):
                    raise ValueError("Nota deve estar entre 0.0 e 10.0.")
                self.model.salvar_nota(aluno_id, avaliacao_id, valor_nota=nota)

            messagebox.showinfo("Sucesso", "Operação realizada com sucesso!")

        except ValueError as ve:
            messagebox.showwarning("Erro", str(ve))
        except Exception as e:
            self.log_error(f"Erro ao salvar nota: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao salvar a nota. Consulte os logs.")

    
    def criar_avaliacao(self):
        """Cria uma nova avaliação."""
        try:
            descricao = self.entry_descricao_avaliacao.get()
            data = self.calendario.get_date()
            tipo = self.combo_tipo_avaliacao_criar.get()

            if not descricao or not data or not tipo:
                raise ValueError("Todos os campos são obrigatórios.")

            # Verifica se a disciplina foi selecionada
            if not self.model.disciplina_selecionada:
                raise ValueError("Nenhuma disciplina selecionada.")

            # Usa o ID da disciplina diretamente
            disciplina_id = self.model.disciplina_selecionada

            # Cria a avaliação
            self.model.criar_avaliacao(disciplina_id, descricao, data, tipo)
            messagebox.showinfo("Sucesso", "Avaliação criada com sucesso!")
            self.carregar_avaliacoes_criadas()
        except ValueError as ve:
            messagebox.showwarning("Erro", str(ve))
        except Exception as e:
            self.log_error(f"Erro ao criar avaliação: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao criar a avaliação. Consulte os logs.")

    def definir_disciplina_selecionada(self, disciplina_id):
        """Define qual disciplina está sendo usada."""
        if any(d[0] == disciplina_id for d in self.disciplinas):  # Verifica se o ID é válido
            self.disciplina_selecionada = disciplina_id  # Define como int
        else:
            raise ValueError("Disciplina inválida.")

    def disciplina_selecionada(self, event):
        """Atualiza a disciplina selecionada no Combobox."""
        try:
            disciplina_nome = self.combo_disciplinas_view.get()
            if disciplina_nome in self.model.disciplinas_dict:
                self.model.definir_disciplina_selecionada(self.model.disciplinas_dict[disciplina_nome])
            else:
                raise ValueError("Disciplina não encontrada.")
        except Exception as e:
            self.log_error(f"Erro ao selecionar disciplina: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao selecionar a disciplina. Consulte os logs.")

    def carregar_avaliacoes(self):
        """Carrega a interface para criar e mostrar avaliações."""
        try:
            ttk.Label(self.tab_avaliacoes, text="Criar Avaliações", font=("Arial", 14), style="TLabel").pack(pady=10)

            # Combobox Disciplina
            if len(self.model.disciplinas) > 1:
                ttk.Label(self.tab_avaliacoes, text="Selecione a Disciplina:", style="TLabel").pack(pady=5)
                self.combo_disciplinas_view = ttk.Combobox(
                    self.tab_avaliacoes,
                    values=[d[1] for d in self.model.disciplinas],
                    state="readonly"
                )
                self.combo_disciplinas_view.pack(pady=5)
                self.combo_disciplinas_view.bind("<<ComboboxSelected>>", lambda _: self.model.definir_disciplina_selecionada(
                    self.model.disciplinas_dict[self.combo_disciplinas_view.get()]
                ))
            elif len(self.model.disciplinas) == 1:
                self.model.definir_disciplina_selecionada(self.model.disciplinas[0][0])

            # Descrição
            ttk.Label(self.tab_avaliacoes, text="Descrição da Avaliação:", style="TLabel").pack(pady=5)
            self.entry_descricao_avaliacao = ttk.Entry(self.tab_avaliacoes)
            self.entry_descricao_avaliacao.pack(pady=5)

            # Data da avaliação
            ttk.Label(self.tab_avaliacoes, text="Data da Avaliação:", style="TLabel").pack(pady=5)
            self.calendario = DateEntry(self.tab_avaliacoes, date_pattern="yyyy-mm-dd")
            self.calendario.pack(pady=5)

            # Tipo de avaliação
            ttk.Label(self.tab_avaliacoes, text="Tipo de Avaliação:", style="TLabel").pack(pady=5)
            self.combo_tipo_avaliacao_criar = ttk.Combobox(self.tab_avaliacoes, values=["AV1", "AV2", "AVS"], state="readonly")
            self.combo_tipo_avaliacao_criar.pack(pady=5)

            # Botão Criar Avaliação
            ttk.Button(self.tab_avaliacoes, text="Criar Avaliação", command=self.criar_avaliacao).pack(pady=10)

                # Tabela de avaliações criadas
            ttk.Label(self.tab_avaliacoes, text="Avaliações Criadas", font=("Arial", 14), style="TLabel").pack(pady=10)
            self.lista_avaliacoes = ttk.Treeview(
                self.tab_avaliacoes,
                columns=("Disciplina", "Data", "Descrição", "Tipo", "Aprovados", "Faltas"),
                show="headings",
                height=10
            )
        
        # Configuração das colunas com larguras específicas
            self.lista_avaliacoes.column("Disciplina", width=150, anchor="w")
            self.lista_avaliacoes.column("Data", width=100, anchor="center")
            self.lista_avaliacoes.column("Descrição", width=250, anchor="w")
            self.lista_avaliacoes.column("Tipo", width=80, anchor="center")
            self.lista_avaliacoes.column("Aprovados", width=80, anchor="center")
            self.lista_avaliacoes.column("Faltas", width=80, anchor="center") 
            
            # Configuração dos cabeçalhos
            self.lista_avaliacoes.heading("Disciplina", text="Disciplina")
            self.lista_avaliacoes.heading("Data", text="Data")
            self.lista_avaliacoes.heading("Descrição", text="Descrição")
            self.lista_avaliacoes.heading("Tipo", text="Tipo")
            self.lista_avaliacoes.heading("Aprovados", text="Aprovados")
            self.lista_avaliacoes.heading("Faltas", text="Faltas")
            
            # Configuração da barra de rolagem vertical
            scrollbar_x = ttk.Scrollbar(self.tab_avaliacoes, orient="horizontal", command=self.lista_avaliacoes.xview)
            self.lista_avaliacoes.configure(xscrollcommand=scrollbar_x.set)
            
            self.lista_avaliacoes.pack(fill="both", expand=True)
            scrollbar_x.pack(fill="x")  # Barra de rolagem horizontal

            self.carregar_avaliacoes_criadas()

        except Exception as e:
            self.log_error(f"Erro ao carregar avaliações: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao carregar a aba de avaliações. Consulte os logs.")

    def carregar_avaliacoes_criadas(self):
        """Recarrega as avaliações futuras na tabela."""
        try:
            self.lista_avaliacoes.delete(*self.lista_avaliacoes.get_children())
            avaliacoes = self.model.buscar_avaliacoes_futuras()
            for avaliacao in avaliacoes:
                avaliacao_id, nome_disciplina, data, descricao, tipo = avaliacao
                aprovados = self.model.contar_alunos_aprovados(avaliacao_id)
                faltas = self.model.contar_faltas(avaliacao_id)
                self.lista_avaliacoes.insert("", "end", values=(nome_disciplina, data, descricao, tipo, aprovados, faltas))

        except Exception as e:
            self.log_error(f"Erro ao recarregar avaliações: {e}")
            messagebox.showerror("Erro", "Ocorreu um erro ao atualizar as avaliações. Consulte os logs.")

    def start(self):
        """Inicia a interface gráfica."""
        self.root.mainloop()