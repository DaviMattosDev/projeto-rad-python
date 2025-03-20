import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('teste.db')
cursor = conn.cursor()

# Criar tabela se ela não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS pessoas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL
)
''')
conn.commit()

# Função para inserir dados no banco
def inserir_dados():
    nome = entry_nome.get()
    idade = entry_idade.get()

    if not nome or not idade:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return

    try:
        idade = int(idade)
    except ValueError:
        messagebox.showwarning("Erro", "A idade deve ser um número inteiro!")
        return

    cursor.execute('INSERT INTO pessoas (nome, idade) VALUES (?, ?)', (nome, idade))
    conn.commit()
    messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
    limpar_campos()
    listar_dados()

# Função para listar dados do banco
def listar_dados():
    listbox_dados.delete(*listbox_dados.get_children())
    cursor.execute('SELECT * FROM pessoas')
    registros = cursor.fetchall()
    for registro in registros:
        listbox_dados.insert("", END, values=registro)

# Função para excluir um registro
def excluir_registro():
    item_selecionado = listbox_dados.selection()
    if not item_selecionado:
        messagebox.showwarning("Erro", "Selecione um registro para excluir!")
        return

    id_selecionado = listbox_dados.item(item_selecionado, "values")[0]
    cursor.execute('DELETE FROM pessoas WHERE id = ?', (id_selecionado,))
    conn.commit()
    messagebox.showinfo("Sucesso", "Registro excluído com sucesso!")
    listar_dados()

# Função para limpar os campos de entrada
def limpar_campos():
    entry_nome.delete(0, END)
    entry_idade.delete(0, END)

# Interface Gráfica
root = Tk()
root.title("Teste Tkinter + SQLite")
root.geometry("600x400")
root.configure(bg="#f0f0f0")

# Cabeçalho institucional
header = Frame(root, bg="#003366", height=50)
header.pack(fill="x")
Label(header, text="Teste Tkinter + SQLite", font=("Arial", 18, "bold"), fg="white", bg="#003366").pack(pady=10)

# Formulário de Cadastro
form_frame = Frame(root, bg="#f0f0f0")
form_frame.pack(pady=20)

Label(form_frame, text="Nome:", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nome = Entry(form_frame, font=("Arial", 10))
entry_nome.grid(row=0, column=1, padx=10, pady=5)

Label(form_frame, text="Idade:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_idade = Entry(form_frame, font=("Arial", 10))
entry_idade.grid(row=1, column=1, padx=10, pady=5)

Button(form_frame, text="Inserir Dados", command=inserir_dados, bg="#003366", fg="white", font=("Arial", 10)).grid(row=2, column=0, columnspan=2, pady=10)

# Lista de Registros
list_frame = Frame(root, bg="#f0f0f0")
list_frame.pack(fill="both", expand=True, padx=20, pady=10)

colunas = ("ID", "Nome", "Idade")
listbox_dados = ttk.Treeview(list_frame, columns=colunas, show="headings", height=10)
for col in colunas:
    listbox_dados.heading(col, text=col)
    listbox_dados.column(col, width=150, anchor="center")
listbox_dados.pack(fill="both", expand=True)

Button(list_frame, text="Listar Dados", command=listar_dados, bg="#003366", fg="white", font=("Arial", 10)).pack(side=LEFT, padx=10, pady=5)
Button(list_frame, text="Excluir Registro", command=excluir_registro, bg="#003366", fg="white", font=("Arial", 10)).pack(side=RIGHT, padx=10, pady=5)

# Iniciar a interface gráfica
root.mainloop()

# Fechar conexão com o banco de dados
conn.close()