import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from login_utils import verificar_login

# Função para exibir a tela de frequência do funcionário


def tela_frequencia_funcionario(frame):
    # Limpar o frame antes de carregar a tela
    for widget in frame.winfo_children():
        widget.destroy()

    # Conexão com o banco de dados
    conn = sqlite3.connect('empresa.db')
    cursor = conn.cursor()

    # Função para localizar funcionário por ID ou nome
    def localizar_funcionario(identificador):
        cursor.execute('''
        SELECT id, nome FROM funcionarios 
        WHERE id = ? OR nome = ?
        ''', (identificador, identificador))
        return cursor.fetchone()  # Retorna (id, nome) ou None se não encontrar

    # Função para registrar entrada
    def registrar_entrada():
        identificador = entry_funcionario_id.get()
        if not identificador:
            messagebox.showwarning(
                "Erro", "Informe o ID ou nome do funcionário!")
            return

        # Localizar funcionário pelo ID ou nome
        resultado = localizar_funcionario(identificador)
        if not resultado:
            messagebox.showerror("Erro", "Funcionário não encontrado!")
            return

        funcionario_id, nome = resultado
        # Verificar situação e data de início do funcionário
        cursor.execute(
            'SELECT situacao, data_inicio FROM funcionarios WHERE id = ?', (funcionario_id,))
        resultado_situacao = cursor.fetchone()
        if not resultado_situacao:
            messagebox.showerror(
                "Erro", "Situação do funcionário não encontrada!")
            return

        situacao, data_inicio = resultado_situacao
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        hoje = datetime.now()

        # Se passaram 3 meses, atualizar para híbrido
        if (hoje - data_inicio).days >= 90 and situacao != "hibrido":
            cursor.execute(
                'UPDATE funcionarios SET situacao = ? WHERE id = ?', ("hibrido", funcionario_id))
            conn.commit()
            situacao = "hibrido"

        # Determinar tipo de trabalho
        dia_semana = hoje.weekday()  # 0 = segunda, 4 = sexta
        tipo_trabalho = "teletrabalho" if situacao == "hibrido" and dia_semana in [
            0, 4] else "presencial"

        # Verificar se já existe uma entrada sem saída registrada
        cursor.execute(
            'SELECT * FROM frequencia WHERE funcionario_id = ? AND data_hora_saida IS NULL', (funcionario_id,))
        registro_aberto = cursor.fetchone()
        if registro_aberto:
            messagebox.showwarning(
                "Erro", "Você já registrou uma entrada hoje. Registre a saída primeiro.")
            return

        # Registrar entrada
        data_hora = hoje.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO frequencia (funcionario_id, nome, data_hora_entrada, tipo_trabalho)
            VALUES (?, ?, ?, ?)
            ''', (funcionario_id, nome, data_hora, tipo_trabalho))
        conn.commit()
        messagebox.showinfo(
            "Sucesso", f"Entrada registrada com sucesso! Tipo: {tipo_trabalho}")
        listar_frequencia()  # Atualiza a lista após registrar entrada

    # Função para registrar saída
    def registrar_saida():
        identificador = entry_funcionario_id.get()
        if not identificador:
            messagebox.showwarning(
                "Erro", "Informe o ID ou nome do funcionário!")
            return

        # Localizar funcionário pelo ID ou nome
        resultado = localizar_funcionario(identificador)
        if not resultado:
            messagebox.showerror("Erro", "Funcionário não encontrado!")
            return

        funcionario_id, _ = resultado

        # Verificar se existe uma entrada sem saída registrada
        cursor.execute(
            'SELECT * FROM frequencia WHERE funcionario_id = ? AND data_hora_saida IS NULL', (funcionario_id,))
        registro_aberto = cursor.fetchone()
        if not registro_aberto:
            messagebox.showwarning(
                "Erro", "Você ainda não registrou uma entrada hoje. Registre a entrada primeiro.")
            return

        # Registrar saída
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            'UPDATE frequencia SET data_hora_saida = ? WHERE funcionario_id = ? AND data_hora_saida IS NULL', (data_hora, funcionario_id))
        conn.commit()
        messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")
        listar_frequencia()  # Atualiza a lista após registrar saída

    # Função para listar frequência
    def listar_frequencia():
        listbox_frequencia.delete(*listbox_frequencia.get_children())
        identificador = entry_funcionario_id.get()
        if not identificador:
            messagebox.showwarning(
                "Erro", "Informe o ID ou nome do funcionário!")
            return

        # Localizar funcionário pelo ID ou nome
        resultado = localizar_funcionario(identificador)
        if not resultado:
            messagebox.showerror("Erro", "Funcionário não encontrado!")
            return

        funcionario_id, _ = resultado

        cursor.execute(
            'SELECT * FROM frequencia WHERE funcionario_id = ?', (funcionario_id,))
        frequencias = cursor.fetchall()
        for frequencia in frequencias:
            entrada = frequencia[3]
            saida = frequencia[4] if frequencia[4] else "Pendente"
            tempo_trabalhado = calcular_tempo_trabalhado(
                entrada, saida) if saida != "Pendente" else "Pendente"
            listbox_frequencia.insert("", END, values=(
                frequencia[0], frequencia[2], entrada, saida, frequencia[5], tempo_trabalhado))

    # Função para calcular tempo trabalhado
    def calcular_tempo_trabalhado(entrada, saida):
        entrada_dt = datetime.strptime(entrada, '%Y-%m-%d %H:%M:%S')
        saida_dt = datetime.strptime(saida, '%Y-%m-%d %H:%M:%S')
        diferenca = saida_dt - entrada_dt
        horas, resto = divmod(diferenca.seconds, 3600)
        minutos = resto // 60
        return f"{horas}h {minutos}m"

    # Interface Gráfica
    main_frame = Frame(frame, bg="#f0f0f0")
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    Label(main_frame, text="ID ou Nome do Funcionário:",
          font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
    entry_funcionario_id = Entry(main_frame, font=("Arial", 10))
    entry_funcionario_id.pack(pady=5)

    Button(main_frame, text="Registrar Entrada", command=registrar_entrada,
           bg="#003366", fg="white", font=("Arial", 10)).pack(pady=10)
    Button(main_frame, text="Registrar Saída", command=registrar_saida,
           bg="#003366", fg="white", font=("Arial", 10)).pack(pady=10)

    list_frame = LabelFrame(main_frame, text="Histórico de Frequência", font=(
        "Arial", 12, "bold"), bg="#f0f0f0", fg="#003366")
    list_frame.pack(fill="both", expand=True, pady=10)

    colunas = ("ID", "Nome", "Entrada", "Saída", "Tipo", "Tempo Trabalhado")
    listbox_frequencia = ttk.Treeview(
        list_frame, columns=colunas, show="headings", height=10)
    for col in colunas:
        listbox_frequencia.heading(col, text=col)
        listbox_frequencia.column(col, width=150, anchor="center")
    listbox_frequencia.pack(fill="both", expand=True, padx=10, pady=5)

    Button(list_frame, text="Atualizar Histórico", command=listar_frequencia,
           bg="#003366", fg="white", font=("Arial", 10)).pack(pady=5)

    # Fechar conexão com o banco de dados ao sair da tela
    frame.bind("<Destroy>", lambda event: conn.close())
