import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
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
    listar_frequencia()  # Atualiza a lista após registrar entrada

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
    listar_frequencia()  # Atualiza a lista após registrar saída

# Função para listar frequência
def listar_frequencia():
    listbox_frequencia.delete(*listbox_frequencia.get_children())
    cursor.execute('SELECT * FROM frequencia WHERE funcionario_id = ?', (entry_funcionario_id.get(),))
    frequencias = cursor.fetchall()
    for frequencia in frequencias:
        entrada = frequencia[2]
        saida = frequencia[3] if frequencia[3] else "Pendente"
        tempo_trabalhado = calcular_tempo_trabalhado(entrada, saida) if saida != "Pendente" else "Pendente"
        listbox_frequencia.insert("", END, values=(frequencia[0], entrada, saida, frequencia[4], tempo_trabalhado))

# Função para calcular tempo trabalhado
def calcular_tempo_trabalhado(entrada, saida):
    entrada_dt = datetime.strptime(entrada, '%Y-%m-%d %H:%M:%S')
    saida_dt = datetime.strptime(saida, '%Y-%m-%d %H:%M:%S')
    diferenca = saida_dt - entrada_dt
    horas, resto = divmod(diferenca.seconds, 3600)
    minutos = resto // 60
    return f"{horas}h {minutos}m"

# Interface Gráfica
root = Tk()
root.title("Registro de Frequência - Funcionário")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Cabeçalho institucional
header = Frame(root, bg="#003366", height=60)
header.pack(fill="x")
Label(header, text="Registro de Frequência", font=("Arial", 18, "bold"), fg="white", bg="#003366").pack(pady=10)

main_frame = Frame(root, bg="#f0f0f0")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

Label(main_frame, text="ID do Funcionário:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
entry_funcionario_id = Entry(main_frame, font=("Arial", 10))
entry_funcionario_id.pack(pady=5)

Button(main_frame, text="Registrar Entrada", command=registrar_entrada, bg="#003366", fg="white", font=("Arial", 10)).pack(pady=10)
Button(main_frame, text="Registrar Saída", command=registrar_saida, bg="#003366", fg="white", font=("Arial", 10)).pack(pady=10)

list_frame = LabelFrame(main_frame, text="Histórico de Frequência", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#003366")
list_frame.pack(fill="both", expand=True, pady=10)

colunas = ("ID", "Entrada", "Saída", "Tipo", "Tempo Trabalhado")
listbox_frequencia = ttk.Treeview(list_frame, columns=colunas, show="headings", height=10)
for col in colunas:
    listbox_frequencia.heading(col, text=col)
    listbox_frequencia.column(col, width=150, anchor="center")
listbox_frequencia.pack(fill="both", expand=True, padx=10, pady=5)

Button(list_frame, text="Atualizar Histórico", command=listar_frequencia, bg="#003366", fg="white", font=("Arial", 10)).pack(pady=5)

root.mainloop()

# Fechar conexão com o banco de dados
conn.close()