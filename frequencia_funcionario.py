import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta

# Conexão com o banco de dados
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

# Função para registrar entrada
def registrar_entrada():
    funcionario_id = entry_funcionario_id.get()

    if not funcionario_id:
        messagebox.showwarning("Erro", "Informe o ID do funcionário!")
        return

    # Verificar se o funcionário existe
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

    # Verificar se já existe uma entrada sem saída registrada
    cursor.execute('SELECT * FROM frequencia WHERE funcionario_id = ? AND data_hora_saida IS NULL', (funcionario_id,))
    registro_aberto = cursor.fetchone()
    if registro_aberto:
        messagebox.showwarning("Erro", "Você já registrou uma entrada hoje. Registre a saída primeiro.")
        return

    # Registrar entrada
    data_hora = hoje.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO frequencia (funcionario_id, data_hora_entrada, tipo_trabalho)
    VALUES (?, ?, ?)
    ''', (funcionario_id, data_hora, tipo_trabalho))
    conn.commit()
    messagebox.showinfo("Sucesso", f"Entrada registrada com sucesso! Tipo: {tipo_trabalho}")

# Função para registrar saída
def registrar_saida():
    funcionario_id = entry_funcionario_id.get()

    if not funcionario_id:
        messagebox.showwarning("Erro", "Informe o ID do funcionário!")
        return

    # Verificar se existe uma entrada sem saída registrada
    cursor.execute('SELECT * FROM frequencia WHERE funcionario_id = ? AND data_hora_saida IS NULL', (funcionario_id,))
    registro_aberto = cursor.fetchone()
    if not registro_aberto:
        messagebox.showwarning("Erro", "Você ainda não registrou uma entrada hoje. Registre a entrada primeiro.")
        return

    # Registrar saída
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('UPDATE frequencia SET data_hora_saida = ? WHERE funcionario_id = ? AND data_hora_saida IS NULL', (data_hora, funcionario_id))
    conn.commit()
    messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")

# Interface Gráfica
root = Tk()
root.title("Registro de Frequência - Funcionário")
root.geometry("400x300")

Label(root, text="ID do Funcionário:").pack(pady=10)
entry_funcionario_id = Entry(root)
entry_funcionario_id.pack(pady=5)

Button(root, text="Registrar Entrada", command=registrar_entrada).pack(pady=10)
Button(root, text="Registrar Saída", command=registrar_saida).pack(pady=10)

root.mainloop()

# Fechar conexão com o banco de dados
conn.close()