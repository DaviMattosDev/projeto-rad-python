import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from login_utils import verificar_login

# Função de login
def abrir_sistema():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if verificar_login(usuario, senha):
        login_window.destroy()
        iniciar_sistema()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

# Iniciar sistema após login
def iniciar_sistema():
    global root
    root = Tk()
    root.title("Gerenciador de Departamentos - Governo Federal")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")  # Fundo claro

    # Cabeçalho institucional
    header = Frame(root, bg="#003366", height=60)
    header.pack(fill="x")
    Label(header, text="Sistema de Gestão de Funcionários", font=("Arial", 18, "bold"), fg="white", bg="#003366").pack(pady=10)

    # Funções do sistema
    def cadastrar_funcionario():
        nome = entry_nome.get()
        cargo = cargo_var.get()
        departamento = departamento_var.get()
        situacao = situacao_var.get()
        data_inicio = entry_data_inicio.get_date().strftime('%Y-%m-%d')

        if not nome or not cargo or not departamento or not situacao or not data_inicio:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        cursor.execute('''
        INSERT INTO funcionarios (nome, cargo, departamento, situacao, data_inicio)
        VALUES (?, ?, ?, ?, ?)
        ''', (nome, cargo, departamento, situacao, data_inicio))
        conn.commit()
        messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
        limpar_campos()

    def listar_funcionarios():
        listbox_funcionarios.delete(*listbox_funcionarios.get_children())
        cursor.execute('SELECT * FROM funcionarios')
        funcionarios = cursor.fetchall()
        for funcionario in funcionarios:
            listbox_funcionarios.insert("", END, values=funcionario)

    def atualizar_funcionario():
        id = entry_id.get()
        campo = campo_var.get()
        novo_valor = novo_valor_var.get()

        if not id or not campo or not novo_valor:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        cursor.execute(f'UPDATE funcionarios SET {campo} = ? WHERE id = ?', (novo_valor, id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
        limpar_campos()

    def excluir_funcionario():
        id = entry_id.get()

        if not id:
            messagebox.showwarning("Erro", "Informe o ID do funcionário!")
            return

        cursor.execute('DELETE FROM funcionarios WHERE id = ?', (id,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
        limpar_campos()

    def limpar_campos():
        entry_nome.delete(0, END)
        cargo_var.set("")
        departamento_var.set("")
        situacao_var.set("")
        entry_id.delete(0, END)
        campo_var.set("")
        novo_valor_var.set("")

    # Interface Gráfica
    main_frame = Frame(root, bg="#f0f0f0")
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Formulário de Cadastro
    form_frame = LabelFrame(main_frame, text="Cadastro de Funcionário", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#003366")
    form_frame.pack(fill="x", pady=10)

    Label(form_frame, text="Nome:", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nome = Entry(form_frame, font=("Arial", 10))
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    Label(form_frame, text="Cargo:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    cargos = ["Analista de Sistemas", "Desenvolvedor", "Gerente de Projetos", "Auxiliar Administrativo"]
    cargo_var = StringVar()
    ttk.Combobox(form_frame, textvariable=cargo_var, values=cargos, font=("Arial", 10)).grid(row=1, column=1, padx=10, pady=5)

    Label(form_frame, text="Departamento:", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    departamentos = ["TI", "Gestão", "Recursos Humanos", "Financeiro"]
    departamento_var = StringVar()
    ttk.Combobox(form_frame, textvariable=departamento_var, values=departamentos, font=("Arial", 10)).grid(row=2, column=1, padx=10, pady=5)

    Label(form_frame, text="Situação:", font=("Arial", 10), bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    situacoes = ["home office", "presencial", "hibrido"]
    situacao_var = StringVar()
    ttk.Combobox(form_frame, textvariable=situacao_var, values=situacoes, font=("Arial", 10)).grid(row=3, column=1, padx=10, pady=5)

    Label(form_frame, text="Data de Início:", font=("Arial", 10), bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_data_inicio = DateEntry(form_frame, date_pattern='yyyy-mm-dd', font=("Arial", 10))
    entry_data_inicio.grid(row=4, column=1, padx=10, pady=5)

    Button(form_frame, text="Cadastrar", command=cadastrar_funcionario, bg="#003366", fg="white", font=("Arial", 10)).grid(row=5, column=0, columnspan=2, pady=10)

    # Lista de Funcionários
    list_frame = LabelFrame(main_frame, text="Lista de Funcionários", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#003366")
    list_frame.pack(fill="both", expand=True, pady=10)

    colunas = ("ID", "Nome", "Cargo", "Departamento", "Situação", "Data Início")
    listbox_funcionarios = ttk.Treeview(list_frame, columns=colunas, show="headings", height=10)
    for col in colunas:
        listbox_funcionarios.heading(col, text=col)
        listbox_funcionarios.column(col, width=100, anchor="center")
    listbox_funcionarios.pack(fill="both", expand=True, padx=10, pady=5)

    Button(list_frame, text="Listar Funcionários", command=listar_funcionarios, bg="#003366", fg="white", font=("Arial", 10)).pack(pady=5)

    # Atualização e Exclusão
    update_frame = LabelFrame(main_frame, text="Atualizar/Excluir Funcionário", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#003366")
    update_frame.pack(fill="x", pady=10)

    Label(update_frame, text="ID do Funcionário:", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_id = Entry(update_frame, font=("Arial", 10))
    entry_id.grid(row=0, column=1, padx=10, pady=5)

    Label(update_frame, text="Campo a Atualizar:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    campos = ["nome", "cargo", "departamento", "situacao", "data_inicio"]
    campo_var = StringVar()
    ttk.Combobox(update_frame, textvariable=campo_var, values=campos, font=("Arial", 10)).grid(row=1, column=1, padx=10, pady=5)

    Label(update_frame, text="Novo Valor:", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    novo_valor_var = StringVar()
    Entry(update_frame, textvariable=novo_valor_var, font=("Arial", 10)).grid(row=2, column=1, padx=10, pady=5)

    Button(update_frame, text="Atualizar", command=atualizar_funcionario, bg="#003366", fg="white", font=("Arial", 10)).grid(row=3, column=0, pady=10)
    Button(update_frame, text="Excluir", command=excluir_funcionario, bg="#003366", fg="white", font=("Arial", 10)).grid(row=3, column=1, pady=10)

    root.mainloop()

# Janela de login
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

login_window = Tk()
login_window.title("Login - Governo Federal")
login_window.geometry("400x300")
login_window.configure(bg="#f0f0f0")

# Cabeçalho institucional
header = Frame(login_window, bg="#003366", height=60)
header.pack(fill="x")
Label(header, text="Sistema de Login", font=("Arial", 18, "bold"), fg="white", bg="#003366").pack(pady=10)

Label(login_window, text="Usuário:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
entry_usuario = Entry(login_window, font=("Arial", 12))
entry_usuario.pack(pady=5)

Label(login_window, text="Senha:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
entry_senha = Entry(login_window, show="*", font=("Arial", 12))
entry_senha.pack(pady=5)

Button(login_window, text="Entrar", command=abrir_sistema, bg="#003366", fg="white", font=("Arial", 12)).pack(pady=20)

login_window.mainloop()

conn.close()