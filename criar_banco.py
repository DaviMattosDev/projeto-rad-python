import sqlite3
from datetime import datetime, timedelta
from unidecode import unidecode  # Importa a biblioteca unidecode

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
    data_inicio TEXT NOT NULL,
    senha TEXT NOT NULL,
    perfil TEXT CHECK(perfil IN ('admin', 'rh', 'gestor', 'funcionario')) DEFAULT 'funcionario'
)
''')
print("Tabela 'funcionarios' criada com sucesso.")

# Criar tabela de frequência
cursor.execute('''
    CREATE TABLE IF NOT EXISTS frequencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    funcionario_id INTEGER NOT NULL,
    nome TEXT NOT NULL,  -- Coluna adicionada para armazenar o nome do funcionário
    data_hora_entrada TEXT NOT NULL,
    data_hora_saida TEXT,
    tipo_trabalho TEXT CHECK(tipo_trabalho IN ('presencial', 'teletrabalho')) DEFAULT 'presencial',
    status TEXT CHECK(status IN ('pendente', 'confirmado', 'nao_confirmado')) DEFAULT 'pendente',
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
)
''')
print("Tabela 'frequencia' criada com sucesso.")

# Criar tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    perfil TEXT CHECK(perfil IN ('admin', 'rh', 'gestor', 'funcionario')) NOT NULL
)
''')
print("Tabela 'usuarios' criada com sucesso.")

# Função para criar automaticamente um usuário para novos funcionários


def criar_usuario_para_funcionario(funcionario_id, nome, senha):
    # Remove caracteres especiais e converte para minúsculas
    usuario = unidecode(nome).lower().replace(
        " ", ".")  # Ex.: "João Silva" → "joao.silva"
    try:
        cursor.execute('''
        INSERT OR IGNORE INTO usuarios (usuario, senha, perfil)
        VALUES (?, ?, ?)
        ''', (usuario, senha, "funcionario"))
        print(f"Usuário '{usuario}' criado com perfil 'funcionario'.")
    except sqlite3.IntegrityError:
        print(f"Usuário '{usuario}' já existe.")


# Inserir alguns dados iniciais na tabela de funcionários
hoje = datetime.now().strftime('%Y-%m-%d')
tres_meses_atras = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')

funcionarios_iniciais = [
    ("João Silva", "Analista de Sistemas", "TI",
     "presencial", tres_meses_atras, "joao123"),
    ("Maria Santos", "Desenvolvedor", "TI", "home office", hoje, "maria123"),
    ("Pedro Almeida", "Gerente de Projetos", "Gestão",
     "presencial", tres_meses_atras, "pedro123"),
    ("Ana Costa", "Auxiliar Administrativo",
     "Recursos Humanos", "hibrido", hoje, "ana123"),
]

# Inserir funcionários e criar usuários automaticamente
for funcionario in funcionarios_iniciais:
    nome, cargo, departamento, situacao, data_inicio, senha = funcionario
    cursor.execute('''
    INSERT OR IGNORE INTO funcionarios (nome, cargo, departamento, situacao, data_inicio, senha)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, cargo, departamento, situacao, data_inicio, senha))
    # Obter o ID do funcionário recém-inserido
    cursor.execute('SELECT id FROM funcionarios WHERE nome = ?', (nome,))
    funcionario_id = cursor.fetchone()[0]
    # Criar usuário para o funcionário
    criar_usuario_para_funcionario(funcionario_id, nome, senha)

print(f"{len(funcionarios_iniciais)} funcionários inseridos ou verificados na tabela 'funcionarios'.")

# Inserir usuários iniciais na tabela de usuários (perfis especiais)
usuarios_iniciais = [
    ("admin", "admin123", "admin"),
    ("rh", "rh123", "rh"),
    ("gestor", "gestor123", "gestor"),
]

cursor.executemany('''
INSERT OR IGNORE INTO usuarios (usuario, senha, perfil)
VALUES (?, ?, ?)
''', usuarios_iniciais)
print(f"{len(usuarios_iniciais)} usuários administrativos inseridos ou verificados na tabela 'usuarios'.")

# Salvar alterações e fechar conexão
conn.commit()
conn.close()
print("Banco de dados configurado com sucesso!")
