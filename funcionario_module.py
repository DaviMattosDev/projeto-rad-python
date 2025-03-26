from tkinter import Toplevel, Label, Button, messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

def funcionario_dashboard(func_win):
    func_win.title("Painel do Funcionário")
    func_win.geometry("500x400")
    func_win.configure(bg="#f0f0f0")

    def on_close():
        conn.close()
        func_win.destroy()

    func_win.protocol("WM_DELETE_WINDOW", on_close)

    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT u.username 
            FROM usuarios u
            WHERE u.perfil = 'funcionario'
        """)
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Erro", "Funcionário não encontrado!")
            return

        username = result[0]

        cursor.execute("""
            SELECT f.nome 
            FROM usuarios u
            JOIN funcionarios f ON u.funcionario_id = f.id
            WHERE u.username = ?
        """, (username,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Erro", "Funcionário não encontrado!")
            return

        nome_funcionario = result[0]

        Label(func_win, text=f"Bem-vindo, {nome_funcionario}!", bg="#f0f0f0", font=("Arial", 18, "bold")).pack(pady=20)
        Label(func_win, text="Registro de Ponto", bg="#f0f0f0", font=("Arial", 16)).pack(pady=10)

        def registrar_entrada():
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO frequencia (funcionario_id, entrada) VALUES (?, ?)", (username, agora))
            conn.commit()
            messagebox.showinfo("Sucesso", "Entrada registrada com sucesso!")

        def registrar_saida():
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("SELECT id FROM frequencia WHERE funcionario_id = ? AND saida IS NULL", (username,))
            registro = cursor.fetchone()
            if not registro:
                messagebox.showwarning("Aviso", "Você ainda não registrou uma entrada ou já registrou a saída!")
                return
            cursor.execute("UPDATE frequencia SET saida = ? WHERE id = ?", (agora, registro[0]))
            conn.commit()
            messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")

        Button(func_win, text="Registrar Entrada", command=registrar_entrada, font=("Arial", 12)).pack(pady=15)
        Button(func_win, text="Registrar Saída", command=registrar_saida, font=("Arial", 12)).pack(pady=15)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar painel do funcionário: {e}")