import sqlite3
from datetime import datetime, timedelta

# Conexão com o banco de dados
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

print("Conectado ao banco de dados 'empresa.db'.")

# Criar tabela de funcionários
cursor.execute('''
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cargo TEXT NOT NULL,
    departamento TEXT NOT NULL,
    situacao TEXT CHECK(situacao IN ('home office', 'presencial', 'hibrido')) NOT NULL,
    data_inicio TEXT NOT NULL
)
''')
print("Tabela 'funcionarios' criada com sucesso.")

# Criar tabela de frequência
cursor.execute('''
CREATE TABLE IF NOT EXISTS frequencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionario_id INTEGER NOT NULL,
    data_hora_entrada TEXT NOT NULL,
    data_hora_saida TEXT,
    tipo_trabalho TEXT CHECK(tipo_trabalho IN ('presencial', 'teletrabalho')) DEFAULT 'presencial',
    status TEXT CHECK(status IN ('pendente', 'confirmado', 'nao_confirmado')) DEFAULT 'pendente',
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
)
''')
print("Tabela 'frequencia' criada com sucesso.")

# Inserir alguns dados iniciais na tabela de funcionários
hoje = datetime.now().strftime('%Y-%m-%d')
tres_meses_atras = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')

funcionarios_iniciais = [
    ("João Silva", "Analista de Sistemas", "TI", "presencial", tres_meses_atras),
    ("Maria Santos", "Desenvolvedor", "TI", "home office", hoje),
    ("Pedro Almeida", "Gerente de Projetos", "Gestão", "presencial", tres_meses_atras),
]

cursor.executemany('''
INSERT INTO funcionarios (nome, cargo, departamento, situacao, data_inicio)
VALUES (?, ?, ?, ?, ?)
''', funcionarios_iniciais)
print(f"{len(funcionarios_iniciais)} funcionários inseridos na tabela 'funcionarios'.")

# Salvar alterações e fechar conexão
conn.commit()
conn.close()
print("Banco de dados configurado com sucesso!")