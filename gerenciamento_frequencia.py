import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from login_utils import verificar_login

# Função de login usando login_utils
def abrir_sistema():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if verificar_login(usuario, senha):
        print("Login bem-sucedido.")
        login_window.destroy()
        iniciar_sistema()
    else:
        print("Login falhou.")
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

def iniciar_sistema():
    global root
    root = Tk()
    root.title("Gerenciamento de Frequência - Governo Federal")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    # Cabeçalho institucional
    header = Frame(root, bg="#003366", height=60)
    header.pack(fill="x")
    Label(header, text="Gerenciamento de Frequência", font=("Arial", 18, "bold"), fg="white", bg="#003366").pack(pady=10)

    # Conexão com o banco de dados
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()
    print("Conexão com o banco de dados estabelecida.")


    def listar_frequencia():
        listbox_frequencia.delete(*listbox_frequencia.get_children())
        cursor.execute('SELECT * FROM frequencia')
        frequencias = cursor.fetchall()
        for frequencia in frequencias:
            status_color = "green" if frequencia[5] == "confirmado" else "yellow" if frequencia[5] == "pendente" else "red"
            listbox_frequencia.insert("", END, values=frequencia, tags=(status_color,))
        listbox_frequencia.tag_configure("green", background="lightgreen")
        listbox_frequencia.tag_configure("yellow", background="yellow")
        listbox_frequencia.tag_configure("red", background="pink")

    def gerar_relatorio_salario():
        # Consulta para listar todos os funcionários, mesmo sem registros
        cursor.execute('''
        SELECT f.nome, COUNT(fr.id) AS dias_trabalhados, 
               SUM(CASE WHEN fr.status = 'confirmado' THEN 8 ELSE 0 END) AS horas_totais
        FROM funcionarios f
        LEFT JOIN frequencia fr ON f.id = fr.funcionario_id
        GROUP BY f.id
        ''')
        relatorio = cursor.fetchall()

        # Gerar arquivo TXT
        with open("relatorio_salario.txt", "w", encoding="utf-8") as arquivo:
            for linha in relatorio:
                nome = linha[0]
                dias_trabalhados = linha[1]
                horas_totais = linha[2] or 0  
                semanas_trabalhadas = dias_trabalhados / 5 if dias_trabalhados > 0 else 0
                horas_semanais = horas_totais / semanas_trabalhadas if semanas_trabalhadas > 0 else 0

                arquivo.write(f"Funcionário: {nome}\n")
                arquivo.write(f"Dias Trabalhados: {dias_trabalhados}\n")
                arquivo.write(f"Horas Totais Trabalhadas: {horas_totais:.2f} horas\n")

                if horas_semanais >= 40 and dias_trabalhados >= 20:  # Verifica 40h/semana e mínimo de 20 dias
                    arquivo.write("Status: Pagamento Aprovado.\n")
                    arquivo.write("Mensagem: O funcionário pode receber o salário.\n\n")
                else:
                    horas_faltantes = 40 - horas_semanais if horas_semanais < 40 else 0
                    dias_faltantes = 20 - dias_trabalhados if dias_trabalhados < 20 else 0
                    arquivo.write("Status: Pagamento em trânsito.\n")
                    arquivo.write(f"Mensagem: Faltam {horas_faltantes:.2f} horas e {dias_faltantes} dias para completar a carga horária.\n\n")

            arquivo.write("Relatório finalizado.")

        messagebox.showinfo("Sucesso", "Relatório gerado com sucesso! Verifique o arquivo 'relatorio_salario.txt'.")

    def alterar_status():
        funcionario_id = entry_funcionario_id.get()
        novo_status = status_var.get()

        if not funcionario_id or not novo_status:
            messagebox.showwarning("Erro", "Informe o ID do funcionário e o novo status!")
            return

        cursor.execute('UPDATE frequencia SET status = ? WHERE funcionario_id = ?', (novo_status, funcionario_id))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Status alterado para '{novo_status}' com sucesso!")
        listar_frequencia()  # Atualiza a lista após alterar o status

    main_frame = Frame(root, bg="#f0f0f0")
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Alteração de Status (Colocado no topo)
    Label(main_frame, text="ID do Funcionário:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
    entry_funcionario_id = Entry(main_frame, font=("Arial", 10))
    entry_funcionario_id.pack(pady=5)

    Label(main_frame, text="Novo Status:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
    status_var = StringVar()
    status_menu = ttk.Combobox(main_frame, textvariable=status_var, values=["pendente", "confirmado", "nao_confirmado"], font=("Arial", 10))
    status_menu.pack(pady=5)

    Button(main_frame, text="Alterar Status", command=alterar_status, bg="#003366", fg="white", font=("Arial", 10)).pack(pady=10)

    Button(main_frame, text="Gerar Relatório de Salário", command=gerar_relatorio_salario, bg="#003366", fg="white", font=("Arial", 10)).pack(pady=10)

    list_frame = LabelFrame(main_frame, text="Lista de Frequência", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#003366")
    list_frame.pack(fill="both", expand=True, pady=10)

    colunas = ("ID", "Funcionário ID", "Entrada", "Saída", "Tipo", "Status")
    listbox_frequencia = ttk.Treeview(list_frame, columns=colunas, show="headings", height=10)
    for col in colunas:
        listbox_frequencia.heading(col, text=col)
        listbox_frequencia.column(col, width=100, anchor="center")
    listbox_frequencia.pack(fill="both", expand=True, padx=10, pady=5)

    Button(list_frame, text="Listar Frequência", command=listar_frequencia, bg="#003366", fg="white", font=("Arial", 10)).pack(pady=5)

    root.mainloop()

    # Fechar conexão com o banco de dados
    conn.close()

# Janela de login
login_window = Tk()
login_window.title("Login - Governo Federal")
login_window.geometry("400x300")
login_window.configure(bg="#f0f0f0")

header = Frame(login_window, bg="#003366", height=60)
header.pack(fill="x")
Label(header, text="Sistema de Frequência", font=("Arial", 18, "bold"), fg="white", bg="#003366").pack(pady=10)

Label(login_window, text="Usuário:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
entry_usuario = Entry(login_window, font=("Arial", 12))
entry_usuario.pack(pady=5)

Label(login_window, text="Senha:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
entry_senha = Entry(login_window, show="*", font=("Arial", 12))
entry_senha.pack(pady=5)

Button(login_window, text="Entrar", command=abrir_sistema, bg="#003366", fg="white", font=("Arial", 12)).pack(pady=20)

login_window.mainloop()