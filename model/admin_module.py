from tkinter import Toplevel, Label, Entry, Button, messagebox, StringVar, ttk
import sqlite3
import hashlib


def admin_dashboard(admin_win):
    # Configurações da janela do administrador
    admin_win.title("Painel do Administrador")
    admin_win.geometry("600x400")
    admin_win.configure(bg="#f0f0f0")

    # Estilo
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")

    # Título
    Label(admin_win, text="Gerenciamento de Usuários",
          bg="#f0f0f0", font=("Arial", 16, "bold")).pack(pady=10)

    # Botões principais
    ttk.Button(admin_win, text="Criar Usuário (RH/Gestor)",
               command=create_user_rh_gestor, style="TButton").pack(pady=5)
    ttk.Button(admin_win, text="Listar Todos os Usuários",
               command=list_all_users, style="TButton").pack(pady=5)
    ttk.Button(admin_win, text="Alterar Perfil de Usuário",
               command=change_user_role, style="TButton").pack(pady=5)
    ttk.Button(admin_win, text="Remover Usuário",
               command=remove_user, style="TButton").pack(pady=5)


def create_user_rh_gestor():
    def save_user():
        username = entry_username.get()
        password = entry_password.get()
        role = role_var.get()

        if not username or not password or not role:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        try:
            # Verificar se o usuário já existe
            cursor.execute(
                "SELECT COUNT(*) FROM usuarios WHERE username = ?", (username,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Erro", "Usuário já existe!")
                return

            # Criar senha hash
            senha_hash = hashlib.sha256(password.encode()).hexdigest()

            # Inserir o novo usuário
            cursor.execute("""
            INSERT INTO usuarios (username, senha, perfil)
            VALUES (?, ?, ?)
            """, (username, senha_hash, role))

            conn.commit()
            messagebox.showinfo(
                "Sucesso", f"Usuário '{role}' criado com sucesso!")
            create_window.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar usuário: {e}")
        finally:
            conn.close()

    # Janela de criação de usuário
    create_window = Toplevel()
    create_window.title("Criar Usuário RH/Gestor")
    create_window.geometry("400x300")
    create_window.configure(bg="#f0f0f0")

    Label(create_window, text="Username:",
          bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    entry_username = Entry(create_window, font=("Arial", 12))
    entry_username.pack(pady=5)

    Label(create_window, text="Senha:", bg="#f0f0f0",
          font=("Arial", 12)).pack(pady=5)
    entry_password = Entry(create_window, show="*", font=("Arial", 12))
    entry_password.pack(pady=5)

    Label(create_window, text="Perfil:", bg="#f0f0f0",
          font=("Arial", 12)).pack(pady=5)
    role_var = StringVar()
    roles = ["rh", "gestor"]
    ttk.Combobox(create_window, textvariable=role_var, values=roles,
                 state="readonly", font=("Arial", 12)).pack(pady=5)

    Button(create_window, text="Salvar", command=save_user,
           bg="#003366", fg="white", font=("Arial", 12)).pack(pady=10)


def list_all_users():
    list_window = Toplevel()
    list_window.title("Lista de Usuários")
    list_window.geometry("800x400")
    list_window.configure(bg="#f0f0f0")

    tree = ttk.Treeview(list_window, columns=(
        "ID", "Username", "Perfil"), show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Perfil", text="Perfil")
    tree.column("ID", width=50, anchor="center")
    tree.column("Username", width=200, anchor="w")
    tree.column("Perfil", width=150, anchor="w")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    conn = sqlite3.connect('sistema.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, perfil FROM usuarios")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()


def change_user_role():
    def update_role():
        username = entry_username.get()
        novo_perfil = novo_perfil_var.get()

        if not username or not novo_perfil:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        try:
            # Verificar se o usuário existe
            cursor.execute(
                'SELECT COUNT(*) FROM usuarios WHERE username = ?', (username,))
            if cursor.fetchone()[0] == 0:  # Se o nome de usuário não existir
                messagebox.showerror("Erro", "Usuário não encontrado!")
                return

            # Atualizar o perfil do usuário
            cursor.execute(
                'UPDATE usuarios SET perfil = ? WHERE username = ?', (novo_perfil, username))
            conn.commit()
            messagebox.showinfo(
                "Sucesso", f"Perfil do usuário '{username}' alterado para '{novo_perfil}'!")
            alterar_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar perfil: {e}")
        finally:
            conn.close()

    # Janela para alterar perfil
    alterar_window = Toplevel()
    alterar_window.title("Alterar Perfil")
    alterar_window.geometry("400x300")
    alterar_window.configure(bg="#f0f0f0")

    Label(alterar_window, text="Username:",
          bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    entry_username = Entry(alterar_window, font=("Arial", 12))
    entry_username.pack(pady=5)

    Label(alterar_window, text="Novo Perfil:",
          bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    novo_perfil_var = StringVar()
    perfis_disponiveis = ["funcionario", "gestor", "rh"]
    ttk.Combobox(alterar_window, textvariable=novo_perfil_var, values=perfis_disponiveis,
                 state="readonly", font=("Arial", 12)).pack(pady=5)

    Button(alterar_window, text="Salvar Alteração", command=update_role, bg="#003366",
           fg="white", font=("Arial", 12)).pack(pady=10)


def remove_user():
    def delete_user():
        user_id = entry_user_id.get()

        if not user_id:
            messagebox.showwarning("Erro", "Informe o ID do usuário!")
            return

        if not messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este usuário?"):
            return

        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
            remove_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover usuário: {e}")
        finally:
            conn.close()

    # Janela de remoção de usuário
    remove_window = Toplevel()
    remove_window.title("Remover Usuário")
    remove_window.geometry("400x200")
    remove_window.configure(bg="#f0f0f0")

    Label(remove_window, text="ID do Usuário:",
          bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    entry_user_id = Entry(remove_window, font=("Arial", 12))
    entry_user_id.pack(pady=5)

    Button(remove_window, text="Remover", command=delete_user,
           bg="#FF0000", fg="white", font=("Arial", 12)).pack(pady=10)
