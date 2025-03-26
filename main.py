from tkinter import Tk, Label, Entry, Button, messagebox, Toplevel
from tkinter import ttk
from database import init_db
from login import authenticate
from admin_module import admin_dashboard
from funcionario_module import funcionario_dashboard
from rh_module import rh_dashboard  # Importa o módulo de RH
from gestor_module import gestor_dashboard  # Importa o módulo de Gestor

# Variável global para rastrear as janelas abertas
current_window = None

def close_current_window():
    """Fecha a janela atual se ela estiver aberta."""
    global current_window
    if current_window and current_window.winfo_exists():
        current_window.destroy()
    current_window = None

def login():
    username = entry_user.get()
    password = entry_pass.get()
    user = authenticate(username, password)
    
    if user:
        user_id, perfil = user
        # Fechar a janela de login
        root.withdraw()  # Esconde a janela de login em vez de destruí-la
        
        # Abrir o painel correspondente ao perfil do usuário
        if perfil == "admin":
            open_admin_dashboard()
        elif perfil == "funcionario":
            open_funcionario_dashboard()
        elif perfil == "rh":
            open_rh_dashboard()
        elif perfil == "gestor":
            open_gestor_dashboard()
        else:
            messagebox.showerror("Erro", "Perfil de usuário desconhecido!")
            root.deiconify()  # Restaura a janela de login
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

def logout():
    """Função para deslogar o usuário e retornar à tela de login."""
    global current_window
    if current_window and current_window.winfo_exists():
        current_window.destroy()
    current_window = None
    root.deiconify()  # Restaura a janela de login

    # Limpar os campos de usuário e senha
    entry_user.delete(0, "end")
    entry_pass.delete(0, "end")

def open_admin_dashboard():
    global current_window
    close_current_window()  # Fecha qualquer janela aberta
    admin_win = Toplevel()
    admin_win.title("Painel do Administrador")
    admin_win.geometry("600x400")
    admin_win.configure(bg="#f0f0f0")
    current_window = admin_win

    def on_close():
        logout()  # Chama a função de logout ao fechar a janela
    admin_win.protocol("WM_DELETE_WINDOW", on_close)

    # Carregar o painel do administrador
    admin_dashboard(admin_win)

    # Botão Deslogar na parte inferior
    Button(admin_win, text="Deslogar", command=logout, font=("Arial", 12), bg="#ff4d4d", fg="white").pack(side="bottom", pady=20)

def open_funcionario_dashboard():
    global current_window
    close_current_window()  # Fecha qualquer janela aberta
    func_win = Toplevel()
    func_win.title("Painel do Funcionário")
    func_win.geometry("500x400")
    func_win.configure(bg="#f0f0f0")
    current_window = func_win

    def on_close():
        logout()  # Chama a função de logout ao fechar a janela
    func_win.protocol("WM_DELETE_WINDOW", on_close)

    # Carregar o painel do funcionário
    funcionario_dashboard(func_win)

    # Botão Deslogar na parte inferior
    Button(func_win, text="Deslogar", command=logout, font=("Arial", 12), bg="#ff4d4d", fg="white").pack(side="bottom", pady=20)

def open_rh_dashboard():
    global current_window
    close_current_window()  # Fecha qualquer janela aberta
    rh_win = Toplevel()
    rh_win.title("Painel de RH")
    rh_win.geometry("600x400")
    rh_win.configure(bg="#f0f0f0")
    current_window = rh_win

    def on_close():
        logout()  # Chama a função de logout ao fechar a janela
    rh_win.protocol("WM_DELETE_WINDOW", on_close)

    # Carregar o painel de RH
    rh_dashboard(rh_win)

    # Botão Deslogar na parte inferior
    Button(rh_win, text="Deslogar", command=logout, font=("Arial", 12), bg="#ff4d4d", fg="white").pack(side="bottom", pady=20)

def open_gestor_dashboard():
    global current_window
    close_current_window()  # Fecha qualquer janela aberta
    gestor_win = Toplevel()
    gestor_win.title("Painel do Gestor")
    gestor_win.geometry("600x400")
    gestor_win.configure(bg="#f0f0f0")
    current_window = gestor_win

    def on_close():
        logout()  # Chama a função de logout ao fechar a janela
    gestor_win.protocol("WM_DELETE_WINDOW", on_close)

    # Carregar o painel do gestor
    gestor_dashboard(gestor_win)

    # Botão Deslogar na parte inferior
    Button(gestor_win, text="Deslogar", command=logout, font=("Arial", 12), bg="#ff4d4d", fg="white").pack(side="bottom", pady=20)

# Inicializa o banco de dados
init_db()

# Interface gráfica da janela de login
root = Tk()
root.title("Login")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure("TLabel", font=("Arial", 14), background="#f0f0f0")
style.configure("TButton", font=("Arial", 12), padding=5)

Label(root, text="Sistema de Login", bg="#f0f0f0", font=("Arial", 18, "bold")).pack(pady=20)

Label(root, text="Usuário:", bg="#f0f0f0", font=("Arial", 14)).pack(pady=5)
entry_user = Entry(root, font=("Arial", 14))
entry_user.pack(pady=5)

Label(root, text="Senha:", bg="#f0f0f0", font=("Arial", 14)).pack(pady=5)
entry_pass = Entry(root, show="*", font=("Arial", 14))
entry_pass.pack(pady=5)

ttk.Button(root, text="Entrar", command=login).pack(pady=20)

root.mainloop()