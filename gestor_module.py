from tkinter import Spinbox, Toplevel, Label, Entry, Button, filedialog, messagebox, StringVar, Listbox
from tkinter import ttk
from tkcalendar import DateEntry  # Importa o DateEntry para o calendário
import sqlite3
from datetime import datetime

def gestor_dashboard(gestor_win):
    # Configurações da janela do gestor
    gestor_win.title("Painel do Gestor")
    gestor_win.geometry("600x400")
    gestor_win.configure(bg="#f0f0f0")

    # Estilo
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")

    Label(gestor_win, text="Gerenciamento de Pontos (Gestor)", bg="#f0f0f0", font=("Arial", 16, "bold")).pack(pady=20)

    # Botões principais
    ttk.Button(gestor_win, text="Ajustar Pontos", command=ajustar_pontos, style="TButton").pack(pady=10)
    ttk.Button(gestor_win, text="Gerar Relatório Individual", command=gerar_relatorio_individual, style="TButton").pack(pady=10)


# Função para ajustar pontos
def ajustar_pontos():
    ajuste_win = Toplevel()
    ajuste_win.title("Ajustar Pontos")
    ajuste_win.geometry("600x500")
    ajuste_win.configure(bg="#f0f0f0")

    Label(ajuste_win, text="Insira o Username do Funcionário:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
    username_entry = Entry(ajuste_win, font=("Arial", 12))
    username_entry.pack(pady=5)

    def buscar_funcionario():
        username = username_entry.get().strip()
        if not username:
            messagebox.showwarning("Erro", "Insira o username do funcionário!")
            return

        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()

        try:
            # Buscar funcionário pelo username
            cursor.execute("""
                SELECT f.id, f.nome 
                FROM usuarios u
                JOIN funcionarios f ON u.funcionario_id = f.id
                WHERE u.username = ?
            """, (username,))
            funcionario = cursor.fetchone()

            if not funcionario:
                messagebox.showerror("Erro", "Funcionário não encontrado!")
                return

            funcionario_id, funcionario_nome = funcionario

            # Criar uma nova janela para ajustar os pontos
            ajuste_detalhes_win = Toplevel()
            ajuste_detalhes_win.title(f"Ajustar Pontos - {funcionario_nome}")
            ajuste_detalhes_win.geometry("600x500")
            ajuste_detalhes_win.configure(bg="#f0f0f0")

            # Exibir últimos pontos registrados
            Label(ajuste_detalhes_win, text="Últimos Pontos Registrados:", bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=10)
            lista_pontos = Listbox(ajuste_detalhes_win, width=80, height=5, font=("Arial", 12))
            lista_pontos.pack(pady=5)

            # Carregar últimos pontos do funcionário
            cursor.execute("""
                SELECT entrada, saida 
                FROM frequencia 
                WHERE funcionario_id = ?
                ORDER BY id DESC LIMIT 5
            """, (funcionario_id,))
            ultimos_pontos = cursor.fetchall()

            if not ultimos_pontos:
                lista_pontos.insert("end", "Nenhum ponto registrado para este funcionário.")
            else:
                for ponto in ultimos_pontos:
                    entrada, saida = ponto
                    saida_text = saida if saida else "Não registrado"
                    lista_pontos.insert("end", f"Entrada: {entrada} | Saída: {saida_text}")

            # Selecionar o tipo de ajuste (entrada ou saída)
            Label(ajuste_detalhes_win, text="Selecione o Tipo de Ajuste:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
            tipo_var = StringVar(value="entrada")
            ttk.Radiobutton(ajuste_detalhes_win, text="Ajustar Entrada", variable=tipo_var, value="entrada").pack(pady=5)
            ttk.Radiobutton(ajuste_detalhes_win, text="Ajustar Saída", variable=tipo_var, value="saida").pack(pady=5)

            # Entrada para ajustar data
            Label(ajuste_detalhes_win, text="Selecione a Data:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
            data_entry = DateEntry(ajuste_detalhes_win, date_pattern='yyyy-mm-dd', font=("Arial", 12))
            data_entry.pack(pady=5)

            # Entrada para ajustar horário
            Label(ajuste_detalhes_win, text="Selecione o Horário:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
            hora_var = StringVar(value="00")
            minuto_var = StringVar(value="00")
            segundo_var = StringVar(value="00")

            frame_horario = ttk.Frame(ajuste_detalhes_win)
            frame_horario.pack(pady=5)

            Spinbox(frame_horario, from_=0, to=23, textvariable=hora_var, width=5, font=("Arial", 12)).grid(row=0, column=0, padx=5)
            Label(frame_horario, text=":", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=1)
            Spinbox(frame_horario, from_=0, to=59, textvariable=minuto_var, width=5, font=("Arial", 12)).grid(row=0, column=2, padx=5)
            Label(frame_horario, text=":", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=3)
            Spinbox(frame_horario, from_=0, to=59, textvariable=segundo_var, width=5, font=("Arial", 12)).grid(row=0, column=4, padx=5)

            # Função para salvar o ajuste
            def salvar_ajuste():
                tipo = tipo_var.get()
                data = data_entry.get_date().strftime('%Y-%m-%d')
                hora = hora_var.get().zfill(2)
                minuto = minuto_var.get().zfill(2)
                segundo = segundo_var.get().zfill(2)
                novo_horario = f"{data} {hora}:{minuto}:{segundo}"

                try:
                    # Primeiro, obter o ID do último registro de frequência
                    cursor.execute("""
                        SELECT id 
                        FROM frequencia 
                        WHERE funcionario_id = ?
                        ORDER BY id DESC LIMIT 1
                    """, (funcionario_id,))
                    ultimo_registro = cursor.fetchone()

                    if not ultimo_registro:
                        messagebox.showerror("Erro", "Nenhum registro de ponto encontrado para este funcionário!")
                        return

                    ultimo_id = ultimo_registro[0]

                    # Agora, atualizar o campo específico (entrada ou saída)
                    cursor.execute(f"""
                        UPDATE frequencia 
                        SET {tipo} = ?
                        WHERE id = ?
                    """, (novo_horario, ultimo_id))

                    conn.commit()
                    messagebox.showinfo("Sucesso", "Pontos ajustados com sucesso!")
                    ajuste_detalhes_win.destroy()

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao ajustar pontos: {e}")

            # Botão para salvar o ajuste
            ttk.Button(ajuste_detalhes_win, text="Salvar Ajuste", command=salvar_ajuste).pack(pady=20)

        finally:
            conn.close()  # Fecha a conexão apenas após concluir todas as operações

    # Botão para buscar o funcionário
    ttk.Button(ajuste_win, text="Buscar Funcionário", command=buscar_funcionario).pack(pady=10)
# Função para gerar relatório individual
def gerar_relatorio_individual():
    relatorio_win = Toplevel()
    relatorio_win.title("Relatório Individual")
    relatorio_win.geometry("600x500")
    relatorio_win.configure(bg="#f0f0f0")

    Label(relatorio_win, text="Insira o Username do Funcionário:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
    username_entry = Entry(relatorio_win, font=("Arial", 12))
    username_entry.pack(pady=5)

    def buscar_funcionario():
        username = username_entry.get().strip()
        if not username:
            messagebox.showwarning("Erro", "Insira o username do funcionário!")
            return

        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()

        try:
            # Buscar funcionário pelo username
            cursor.execute("""
                SELECT f.id, f.nome 
                FROM usuarios u
                JOIN funcionarios f ON u.funcionario_id = f.id
                WHERE u.username = ?
            """, (username,))
            funcionario = cursor.fetchone()

            if not funcionario:
                messagebox.showerror("Erro", "Funcionário não encontrado!")
                return

            funcionario_id, funcionario_nome = funcionario

            # Carregar registros de frequência do funcionário
            cursor.execute("""
                SELECT entrada, saida 
                FROM frequencia 
                WHERE funcionario_id = ?
            """, (funcionario_id,))
            registros = cursor.fetchall()

            total_horas = 0
            relatorio_texto = f"Relatório de Ponto - {funcionario_nome}\n"

            for registro in registros:
                entrada = datetime.strptime(registro[0], "%Y-%m-%d %H:%M:%S")
                saida = datetime.strptime(registro[1], "%Y-%m-%d %H:%M:%S") if registro[1] else None

                if saida:
                    horas_trabalhadas = (saida - entrada).total_seconds() / 3600
                    total_horas += horas_trabalhadas
                    relatorio_texto += f"Entrada: {registro[0]} | Saída: {registro[1]} | Horas: {horas_trabalhadas:.2f}\n"
                else:
                    relatorio_texto += f"Entrada: {registro[0]} | Saída: Não registrado\n"

            relatorio_texto += f"\nTotal de Horas Trabalhadas: {total_horas:.2f} horas\n"

            if total_horas >= 40:
                relatorio_texto += "Status: Funcionário cumpriu as 40 horas semanais e está apto a receber o salário."
            else:
                relatorio_texto += "Status: Funcionário NÃO cumpriu as 40 horas semanais."

            # Salvar relatório em um arquivo .txt
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(relatorio_texto)
                messagebox.showinfo("Sucesso", "Relatório gerado e salvo com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

        finally:
            conn.close()  # Fecha a conexão apenas após concluir todas as operações

    # Botão para buscar o funcionário
    ttk.Button(relatorio_win, text="Buscar Funcionário", command=buscar_funcionario).pack(pady=10)