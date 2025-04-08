from tkinter import Toplevel, Label, Entry, Button, messagebox, StringVar, Listbox, Scrollbar
from tkinter import ttk
from tkcalendar import DateEntry  # Importa o DateEntry para o calendário
import sqlite3
import hashlib

def rh_dashboard(rh_win):
    # Configurações da janela do RH
    rh_win.title("Painel de RH")
    rh_win.geometry("600x400")
    rh_win.configure(bg="#f0f0f0")

    # Estilo
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")

    Label(rh_win, text="Gerenciamento de Funcionários (RH)", bg="#f0f0f0", font=("Arial", 16, "bold")).pack(pady=10)

    # Botões principais
    ttk.Button(rh_win, text="Cadastrar Funcionário", command=add_funcionario, style="TButton").pack(pady=10)
    ttk.Button(rh_win, text="Listar Funcionários", command=list_funcionarios, style="TButton").pack(pady=10)
    ttk.Button(rh_win, text="Remover Funcionário", command=remove_funcionario, style="TButton").pack(pady=10)

# Função para adicionar um novo funcionário
def add_funcionario():
    add_win = Toplevel()
    add_win.title("Adicionar Funcionário")
    add_win.geometry("550x600")
    add_win.configure(bg="#f0f0f0")

    # Criar frame de formulário
    form_frame = ttk.LabelFrame(add_win, text="Cadastro de Funcionário")
    form_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Configurar colunas para expansão
    form_frame.grid_columnconfigure(1, weight=1)

    # Nome
    Label(form_frame, text="Nome Completo:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    nome_entry = Entry(form_frame, font=("Arial", 12))
    nome_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    # Cargo
    Label(form_frame, text="Cargo:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    cargo_var = StringVar()
    cargo_combobox = ttk.Combobox(form_frame, textvariable=cargo_var, values=["Analista de Sistemas", "Desenvolvedor", "Gerente de Projetos", "Auxiliar Administrativo"], font=("Arial", 12))
    cargo_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Departamento
    Label(form_frame, text="Departamento:", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    departamento_var = StringVar()
    departamento_combobox = ttk.Combobox(form_frame, textvariable=departamento_var, values=["TI", "Gestão", "Recursos Humanos", "Financeiro"], font=("Arial", 12))
    departamento_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Situação
    Label(form_frame, text="Situação:", bg="#f0f0f0", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    situacao_var = StringVar()
    situacao_combobox = ttk.Combobox(form_frame, textvariable=situacao_var, values=["home office", "presencial", "híbrido"], font=("Arial", 12))
    situacao_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    # Data de Início
    Label(form_frame, text="Data de Início:", bg="#f0f0f0", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_data_inicio = DateEntry(form_frame, date_pattern='yyyy-mm-dd', font=("Arial", 12))
    entry_data_inicio.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    # Senha
    Label(form_frame, text="Senha:", bg="#f0f0f0", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_senha = Entry(form_frame, show="*", font=("Arial", 12))
    entry_senha.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    # Confirmar Senha
    Label(form_frame, text="Confirmar Senha:", bg="#f0f0f0", font=("Arial", 12)).grid(row=6, column=0, padx=10, pady=5, sticky="w")
    entry_confirmar_senha = Entry(form_frame, show="*", font=("Arial", 12))
    entry_confirmar_senha.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

    def salvar_funcionario():
        nome = nome_entry.get()
        cargo = cargo_var.get()
        departamento = departamento_var.get()
        situacao = situacao_var.get()
        data_inicio = entry_data_inicio.get_date().strftime('%Y-%m-%d')
        senha = entry_senha.get()
        confirmar_senha = entry_confirmar_senha.get()

        if not nome or not cargo or not departamento or not situacao or not data_inicio or not senha or not confirmar_senha:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        if senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return

        # Gerar o username baseado no nome completo (ex: davi.mattos)
        username = nome.lower().replace(" ", ".")
        # Gerar o hash da senha
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()

        try:
            # Inserir o funcionário na tabela funcionarios
            cursor.execute("""
                INSERT INTO funcionarios (nome, cargo, departamento, situacao, data_inicio, senha)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome, cargo, departamento, situacao, data_inicio, senha))

            # Pegar o ID do funcionário inserido
            funcionario_id = cursor.lastrowid

            # Inserir o usuário na tabela usuarios com perfil 'funcionario' e senha com hash
            cursor.execute("""
                INSERT INTO usuarios (username, senha, perfil, funcionario_id)
                VALUES (?, ?, ?, ?)
            """, (username, senha_hash, "funcionario", funcionario_id))

            conn.commit()
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            add_win.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar funcionário: {e}")
        finally:
            conn.close()

    # Botão Salvar
    ttk.Button(form_frame, text="Salvar", command=salvar_funcionario).grid(row=7, column=0, columnspan=2, pady=20)

# Função para listar funcionários
def list_funcionarios():
    list_win = Toplevel()
    list_win.title("Lista de Funcionários")
    list_win.geometry("700x400")
    list_win.configure(bg="#f0f0f0")

    listbox = ttk.Treeview(list_win, columns=("ID", "Nome", "Cargo", "Departamento", "Situação", "Data Início"), show="headings", height=15)
    listbox.heading("ID", text="ID")
    listbox.heading("Nome", text="Nome")
    listbox.heading("Cargo", text="Cargo")
    listbox.heading("Departamento", text="Departamento")
    listbox.heading("Situação", text="Situação")
    listbox.heading("Data Início", text="Data Início")
    listbox.column("ID", width=50, anchor="center")
    listbox.column("Nome", width=150, anchor="w")
    listbox.column("Cargo", width=150, anchor="w")
    listbox.column("Departamento", width=100, anchor="w")
    listbox.column("Situação", width=100, anchor="w")
    listbox.column("Data Início", width=100, anchor="center")
    listbox.pack(side="left", fill="y", padx=10, pady=10)

    scrollbar = ttk.Scrollbar(list_win, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    # Carregar funcionários
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, cargo, departamento, situacao, data_inicio FROM funcionarios")
    for row in cursor.fetchall():
        listbox.insert("", "end", values=row)
    conn.close()

# Função para remover funcionários
def remove_funcionario():
    remove_win = Toplevel()
    remove_win.title("Remover Funcionário")
    remove_win.geometry("500x400")
    remove_win.configure(bg="#f0f0f0")

    Label(remove_win, text="Método de Remoção:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)

    # Variável para armazenar o método de remoção
    metodo_var = StringVar(value="id")

    # Caixa de seleção para escolher o método de remoção
    check_id = ttk.Checkbutton(remove_win, text="Por ID", variable=metodo_var, onvalue="id", offvalue="")
    check_id.pack(pady=5)
    check_username = ttk.Checkbutton(remove_win, text="Por Username", variable=metodo_var, onvalue="username", offvalue="")
    check_username.pack(pady=5)

    Label(remove_win, text="Valor:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    valor_entry = Entry(remove_win, font=("Arial", 12))
    valor_entry.pack(pady=5)

    # Listbox para exibir o funcionário encontrado
    listbox = Listbox(remove_win, width=80, height=5, font=("Arial", 12))
    listbox.pack(pady=10)

    scrollbar = Scrollbar(remove_win, orient="vertical")
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    def buscar_funcionario():
        metodo = metodo_var.get()
        valor = valor_entry.get().strip()

        if not valor:
            messagebox.showwarning("Aviso", "Insira um valor para buscar!")
            return

        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()

        try:
            if metodo == "id":
                cursor.execute("SELECT id, nome, cargo, departamento FROM funcionarios WHERE id = ?", (valor,))
            elif metodo == "username":
                cursor.execute("""
                    SELECT f.id, f.nome, f.cargo, f.departamento 
                    FROM funcionarios f
                    JOIN usuarios u ON f.id = u.funcionario_id
                    WHERE u.username = ?
                """, (valor,))
            else:
                messagebox.showwarning("Aviso", "Selecione um método de remoção!")
                return

            funcionario = cursor.fetchone()

            # Limpar o Listbox antes de exibir novos resultados
            listbox.delete(0, "end")

            if funcionario:
                listbox.insert("end", f"ID: {funcionario[0]} | Nome: {funcionario[1]} | Cargo: {funcionario[2]} | Departamento: {funcionario[3]}")
            else:
                listbox.insert("end", "Nenhum funcionário encontrado.")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar funcionário: {e}")
        finally:
            conn.close()

    def remover():
        metodo = metodo_var.get()
        valor = valor_entry.get().strip()

        if not valor:
            messagebox.showwarning("Aviso", "Insira um valor para remover!")
            return

        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()

        try:
            if metodo == "id":
                cursor.execute("DELETE FROM funcionarios WHERE id = ?", (valor,))
            elif metodo == "username":
                cursor.execute("""
                    DELETE FROM funcionarios 
                    WHERE id = (
                        SELECT funcionario_id FROM usuarios WHERE username = ?
                    )
                """, (valor,))

            if cursor.rowcount == 0:
                messagebox.showwarning("Aviso", "Nenhum funcionário encontrado com o valor informado!")
            else:
                conn.commit()
                messagebox.showinfo("Sucesso", "Funcionário removido com sucesso!")

            remove_win.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover funcionário: {e}")
        finally:
            conn.close()

    # Botões Buscar e Remover
    ttk.Button(remove_win, text="Buscar", command=buscar_funcionario).pack(pady=5)
    ttk.Button(remove_win, text="Remover", command=remover).pack(pady=10)