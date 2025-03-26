from tkinter import Entry, Listbox, Scrollbar, StringVar, Toplevel, Label, Button, messagebox
from tkinter import ttk
import sqlite3

def rh_dashboard(rh_win):
    # Configurações da janela do RH
    rh_win.title("Painel de RH")
    rh_win.geometry("600x400")
    rh_win.configure(bg="#f0f0f0")

    # Estilo
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")

    Label(rh_win, text="Gerenciamento de Funcionários (RH)", bg="#f0f0f0", font=("Arial", 16, "bold")).pack(pady=20)

    # Botões principais
    ttk.Button(rh_win, text="Cadastrar Funcionário", command=add_funcionario, style="TButton").pack(pady=10)
    ttk.Button(rh_win, text="Remover Funcionário", command=remove_funcionario, style="TButton").pack(pady=10)

def add_funcionario():
    add_win = Toplevel()
    add_win.title("Adicionar Funcionário")
    add_win.geometry("550x600")
    add_win.configure(bg="#f0f0f0")

    # Criar frame de formulário
    form_frame = ttk.LabelFrame(add_win, text="Cadastro de Funcionário")
    form_frame.pack(fill="both", expand=True, padx=10, pady=10)

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

    # Senha
    Label(form_frame, text="Senha:", bg="#f0f0f0", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_senha = Entry(form_frame, show="*", font=("Arial", 12))
    entry_senha.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    def salvar_funcionario():
        nome = nome_entry.get()
        cargo = cargo_var.get()
        departamento = departamento_var.get()
        senha = entry_senha.get()

        if not nome or not cargo or not departamento or not senha:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()

        try:
            # Inserir o funcionário na tabela funcionarios
            cursor.execute("""
                INSERT INTO funcionarios (nome, cargo, departamento, situacao, data_inicio, senha)
                VALUES (?, ?, ?, 'presencial', DATE('now'), ?)
            """, (nome, cargo, departamento, senha))

            conn.commit()
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            add_win.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar funcionário: {e}")
        finally:
            conn.close()

    # Botão Salvar
    ttk.Button(form_frame, text="Salvar", command=salvar_funcionario).grid(row=4, column=0, columnspan=2, pady=20)

def remove_funcionario():
    remove_win = Toplevel()
    remove_win.title("Remover Funcionário")
    remove_win.geometry("500x400")
    remove_win.configure(bg="#f0f0f0")

    Label(remove_win, text="Selecione o funcionário para remover:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)

    listbox = Listbox(remove_win, width=60, height=10, font=("Arial", 12))
    listbox.pack(pady=10)

    scrollbar = Scrollbar(remove_win, orient="vertical")
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)

    # Carregar funcionários na lista
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM funcionarios")
    funcionarios = cursor.fetchall()
    conn.close()

    for funcionario in funcionarios:
        listbox.insert("end", f"{funcionario[1]}")

    def remover():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Selecione um funcionário!")
            return

        funcionario_id = funcionarios[selected_index[0]][0]

        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM funcionarios WHERE id = ?", (funcionario_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Funcionário removido com sucesso!")
            remove_win.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover funcionário: {e}")
        finally:
            conn.close()

    ttk.Button(remove_win, text="Remover", command=remover).pack(pady=10)