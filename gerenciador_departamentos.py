from tkinter import *
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3


def tela_gerenciador_departamentos(frame):
    # Limpar o frame antes de carregar a tela
    for widget in frame.winfo_children():
        widget.destroy()

    # Conexão com o banco de dados
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()

    # Criar Canvas e Scrollbar
    canvas = Canvas(frame, bg="#f0f0f0")
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#f0f0f0")

    # Configurar o Canvas para usar o Scrollbar
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Empacotar o Canvas e o Scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Funções do sistema
    def cadastrar_funcionario():
        nome = entry_nome.get()
        cargo = cargo_var.get()
        departamento = departamento_var.get()
        situacao = situacao_var.get()
        data_inicio = entry_data_inicio.get_date().strftime('%Y-%m-%d')
        senha = entry_senha.get()
        confirmar_senha = entry_confirmar_senha.get()

        # Verificar se todos os campos estão preenchidos
        if not nome or not cargo or not departamento or not situacao or not data_inicio or not senha or not confirmar_senha:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        # Verificar se as senhas coincidem
        if senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return

        # Inserir o funcionário no banco de dados
        cursor.execute('''
        INSERT INTO funcionarios (nome, cargo, departamento, situacao, data_inicio, senha)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, cargo, departamento, situacao, data_inicio, senha))
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
        cursor.execute(
            f'UPDATE funcionarios SET {campo} = ? WHERE id = ?', (novo_valor, id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
        limpar_campos()
        listar_funcionarios()  # Atualiza a lista após a alteração

    def excluir_funcionario():
        id = entry_id.get()
        if not id:
            messagebox.showwarning("Erro", "Informe o ID do funcionário!")
            return
        cursor.execute('DELETE FROM funcionarios WHERE id = ?', (id,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
        limpar_campos()
        listar_funcionarios()  # Atualiza a lista após a exclusão

    def limpar_campos():
        entry_nome.delete(0, END)
        cargo_var.set("")
        departamento_var.set("")
        situacao_var.set("")
        entry_id.delete(0, END)
        campo_var.set("")
        novo_valor_var.set("")
        entry_senha.delete(0, END)  # Limpar campo de senha
        # Limpar campo de confirmação de senha
        entry_confirmar_senha.delete(0, END)

    def preencher_novo_valor(*args):
        campo = campo_var.get()
        if campo == "cargo":
            novo_valor_menu['values'] = ["Analista de Sistemas",
                                         "Desenvolvedor", "Gerente de Projetos", "Auxiliar Administrativo"]
        elif campo == "departamento":
            novo_valor_menu['values'] = [
                "TI", "Gestão", "Recursos Humanos", "Financeiro"]
        elif campo == "situacao":
            novo_valor_menu['values'] = [
                "home office", "presencial", "hibrido"]
        else:
            novo_valor_menu['values'] = []

    # Formulário de Cadastro
    form_frame = LabelFrame(scrollable_frame, text="Cadastro de Funcionário", font=(
        "Arial", 12, "bold"), bg="#f0f0f0", fg="#003366")
    form_frame.pack(fill="x", pady=10)
    Label(form_frame, text="Nome:", font=("Arial", 10), bg="#f0f0f0").grid(
        row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nome = Entry(form_frame, font=("Arial", 10))
    entry_nome.grid(row=0, column=1, padx=10, pady=5)
    Label(form_frame, text="Cargo:", font=("Arial", 10), bg="#f0f0f0").grid(
        row=1, column=0, padx=10, pady=5, sticky="w")
    cargos = ["Analista de Sistemas", "Desenvolvedor",
              "Gerente de Projetos", "Auxiliar Administrativo"]
    cargo_var = StringVar()
    ttk.Combobox(form_frame, textvariable=cargo_var, values=cargos,
                 font=("Arial", 10)).grid(row=1, column=1, padx=10, pady=5)
    Label(form_frame, text="Departamento:", font=("Arial", 10), bg="#f0f0f0").grid(
        row=2, column=0, padx=10, pady=5, sticky="w")
    departamentos = ["TI", "Gestão", "Recursos Humanos", "Financeiro"]
    departamento_var = StringVar()
    ttk.Combobox(form_frame, textvariable=departamento_var, values=departamentos, font=(
        "Arial", 10)).grid(row=2, column=1, padx=10, pady=5)
    Label(form_frame, text="Situação:", font=("Arial", 10), bg="#f0f0f0").grid(
        row=3, column=0, padx=10, pady=5, sticky="w")
    situacoes = ["home office", "presencial", "hibrido"]
    situacao_var = StringVar()
    ttk.Combobox(form_frame, textvariable=situacao_var, values=situacoes, font=(
        "Arial", 10)).grid(row=3, column=1, padx=10, pady=5)
    Label(form_frame, text="Data de Início:", font=("Arial", 10),
          bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_data_inicio = DateEntry(
        form_frame, date_pattern='yyyy-mm-dd', font=("Arial", 10))
    entry_data_inicio.grid(row=4, column=1, padx=10, pady=5)

    # Adicionar campos de senha
    Label(form_frame, text="Senha:", font=("Arial", 10), bg="#f0f0f0").grid(
        row=5, column=0, padx=10, pady=5, sticky="w")
    entry_senha = Entry(form_frame, show="*", font=("Arial", 10))
    entry_senha.grid(row=5, column=1, padx=10, pady=5)
    Label(form_frame, text="Confirmar Senha:", font=("Arial", 10), bg="#f0f0f0").grid(
        row=6, column=0, padx=10, pady=5, sticky="w")
    entry_confirmar_senha = Entry(form_frame, show="*", font=("Arial", 10))
    entry_confirmar_senha.grid(row=6, column=1, padx=10, pady=5)

    Button(form_frame, text="Cadastrar", command=cadastrar_funcionario, bg="#003366",
           fg="white", font=("Arial", 10)).grid(row=7, column=0, columnspan=2, pady=10)

    # Lista de Funcionários
    list_frame = LabelFrame(scrollable_frame, text="Lista de Funcionários", font=(
        "Arial", 12, "bold"), bg="#f0f0f0", fg="#003366")
    list_frame.pack(fill="both", expand=True, pady=10)
    colunas = ("ID", "Nome", "Cargo", "Departamento",
               "Situação", "Data Início", "Perfil")
    listbox_funcionarios = ttk.Treeview(
        list_frame, columns=colunas, show="headings", height=10)
    for col in colunas:
        listbox_funcionarios.heading(col, text=col)
        listbox_funcionarios.column(col, width=100, anchor="center")
    listbox_funcionarios.pack(fill="both", expand=True, padx=10, pady=5)
    Button(list_frame, text="Listar Funcionários", command=listar_funcionarios,
           bg="#003366", fg="white", font=("Arial", 10)).pack(pady=5)

    # Atualização e Exclusão
    update_frame = LabelFrame(scrollable_frame, text="Atualizar/Excluir Funcionário",
                              font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#003366")
    update_frame.pack(fill="x", pady=10)
    Label(update_frame, text="ID do Funcionário:", font=("Arial", 10),
          bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_id = Entry(update_frame, font=("Arial", 10))
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    Label(update_frame, text="Campo a Atualizar:", font=("Arial", 10),
          bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    campos = ["nome", "cargo", "departamento",
              "situacao", "data_inicio", "senha"]
    campo_var = StringVar()
    ttk.Combobox(update_frame, textvariable=campo_var, values=campos, font=(
        "Arial", 10)).grid(row=1, column=1, padx=10, pady=5)
    Label(update_frame, text="Novo Valor:", font=("Arial", 10), bg="#f0f0f0").grid(
        row=2, column=0, padx=10, pady=5, sticky="w")
    novo_valor_var = StringVar()
    novo_valor_menu = ttk.Combobox(
        update_frame, textvariable=novo_valor_var, font=("Arial", 10))
    novo_valor_menu.grid(row=2, column=1, padx=10, pady=5)
    campo_var.trace_add("write", lambda *args: preencher_novo_valor())
    Button(update_frame, text="Atualizar", command=atualizar_funcionario,
           bg="#003366", fg="white", font=("Arial", 10)).grid(row=3, column=0, pady=10)
    Button(update_frame, text="Excluir", command=excluir_funcionario,
           bg="#003366", fg="white", font=("Arial", 10)).grid(row=3, column=1, pady=10)
