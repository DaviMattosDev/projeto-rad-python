import sqlite3
import hashlib

def authenticate(username, password):
    senha_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, perfil FROM usuarios WHERE username = ? AND senha = ?
    """, (username, senha_hash))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return user  # Retorna (id, perfil)
    else:
        return None