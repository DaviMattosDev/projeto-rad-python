from controller.database import init_db
from view.displays import root

# Inicializa o banco de dados
init_db()

# Executa a interface gráfica
if __name__ == "__main__":
    root.mainloop()