import sqlite3
from tkinter import *
from tkinter import messagebox
from login_utils import verificar_login
from datetime import datetime, timedelta

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
    root.title("Gerenciamento de Frequência")
    root.geometry("600x500")

    # Funções do sistema
    def registrar_ponto_entrada():
        funcionario_id = entry_funcionario_id.get()

        if not funcionario_id:
            messagebox.showwarning("Erro", "Informe o ID do funcionário!")
            return

        # Verificar situação do funcionário
        cursor.execute('SELECT situacao, data_inicio FROM funcionarios WHERE id = ?', (funcionario_id,))
        resultado = cursor.fetchone()
        if not resultado:
            messagebox.showerror("Erro", "Funcionário não encontrado!")
            return

        situacao, data_inicio = resultado
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        hoje = datetime.now()

        # Se passaram 3 meses, atualizar para híbrido
        if (hoje - data_inicio).days >= 90 and situacao != "hibrido":
            cursor.execute('UPDATE funcionarios SET situacao = ? WHERE id = ?', ("hibrido", funcionario_id))
            conn.commit()
            situacao = "hibrido"

        # Determinar tipo de trabalho
        dia_semana = hoje.weekday()  # 0 = segunda, 4 = sexta
        tipo_trabalho = "teletrabalho" if situacao == "hibrido" and dia_semana in [0, 4] else "presencial"

        # Registrar entrada
        data_hora = hoje.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
        INSERT INTO frequencia (funcionario_id, data_hora_entrada, tipo_trabalho)
        VALUES (?, ?, ?)
        ''', (funcionario_id, data_hora, tipo_trabalho))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Entrada registrada com sucesso! Tipo: {tipo_trabalho}")

    def registrar_ponto_saida():
        funcionario_id = entry_funcionario_id.get()

        if not funcionario_id:
            messagebox.showwarning("Erro", "Informe o ID do funcionário!")
            return

        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('UPDATE frequencia SET data_hora_saida = ? WHERE funcionario_id = ? AND data_hora_saida IS NULL', (data_hora, funcionario_id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")

    def consultar_frequencia():
        funcionario_id = entry_funcionario_id.get()

        if not funcionario_id:
            messagebox.showwarning("Erro", "Informe o ID do funcionário!")
            return

        cursor.execute('SELECT * FROM frequencia WHERE funcionario_id = ?', (funcionario_id,))
        frequencias = cursor.fetchall()
        listbox_frequencia.delete(0, END)
        for frequencia in frequencias:
            listbox_frequencia.insert(END, f"ID: {frequencia[0]}, Entrada: {frequencia[2]}, Saída: {frequencia[3]}, Tipo: {frequencia[4]}")

    # Interface Gráfica
    Label(root, text="ID do Funcionário:").grid(row=0, column=0, padx=10, pady=5)
    entry_funcionario_id = Entry(root)
    entry_funcionario_id.grid(row=0, column=1, padx=10, pady=5)

    Button(root, text="Registrar Entrada", command=registrar_ponto_entrada).grid(row=1, column=0, columnspan=2, pady=5)
    Button(root, text="Registrar Saída", command=registrar_ponto_saida).grid(row=2, column=0, columnspan=2, pady=5)

    Label(root, text="Histórico de Frequência:").grid(row=3, column=0, columnspan=2)
    listbox_frequencia = Listbox(root, width=80, height=10)
    listbox_frequencia.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
    Button(root, text="Consultar Frequência", command=consultar_frequencia).grid(row=5, column=0, columnspan=2, pady=5)

    root.mainloop()

# Janela de login
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

login_window = Tk()
login_window.title("Login")
login_window.geometry("300x200")

Label(login_window, text="Usuário:").pack(pady=5)
entry_usuario = Entry(login_window)
entry_usuario.pack(pady=5)

Label(login_window, text="Senha:").pack(pady=5)
entry_senha = Entry(login_window, show="*")
entry_senha.pack(pady=5)

Button(login_window, text="Entrar", command=abrir_sistema).pack(pady=10)

login_window.mainloop()

conn.close()