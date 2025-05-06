43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
⌄
# 🎓 Sistema de Gerenciamento Escolar
## 🗃️ Banco de Dados SQLite (`extensao.db`)

Tabelas criadas automaticamente na primeira execução:

### `usuarios`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| nome_completo | TEXT | Nome do usuário |
| email | TEXT | Email único |
| senha | TEXT | Senha (armazenada como texto plano - recomenda-se hash futuramente) |
| tipo_usuario | TEXT | 'admin', 'professor' ou 'aluno' |
| matricula | TEXT | Matrícula única |
| cpf | TEXT | CPF do usuário |
| data_nascimento | DATE | Data de nascimento |

### `disciplinas`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| nome | TEXT | Nome da disciplina |
| descricao | TEXT | Descrição opcional |
| professor_id | INTEGER | ID do professor que ministra |

### `frequencias`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| aluno_id | INTEGER | ID do aluno |
| disciplina_id | INTEGER | ID da disciplina |
| data_aula | DATE | Data da aula |
| presente | BOOLEAN | True = presente / False = falta |

### `avaliacoes`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| disciplina_id | INTEGER | ID da disciplina |
| data_avaliacao | DATE | Data da avaliação |
| descricao | TEXT | Descrição da avaliação |
| tipo_avaliacao | TEXT | AV1, AV2, AVS |

### `notas`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| aluno_id | INTEGER | ID do aluno |
| disciplina_id | INTEGER | ID da disciplina |
| avaliacao_id | INTEGER | ID da avaliação |
| valor_nota | REAL | Valor da nota lançada |
| faltou | BOOLEAN | Se o aluno faltou na avaliação |

---

## 📁 Estrutura do Projeto

projeto-rad-python/
│
├── controllers/
│ └── auth_controller.py # Controla login e navegação entre telas
│
├── models/
│ ├── usuario.py # Lógica de usuários e autenticação
│ ├── disciplina.py # CRUD de disciplinas e professores
│ ├── aluno_model.py # Manipulação de frequências e notas
│ └── remover_aluno_professor_model.py # Lógica para desvincular aluno
│
├── views/
│ ├── login_view.py # Tela de login
│ ├── admin_view.py # Painel do administrador
│ ├── professor_view.py # Acesso do professor
│ ├── aluno_view.py # Acesso do aluno
│ ├── relatorios_view.py # Relatórios com gráficos e exportações
│ ├── cadastrar_usuario_view.py # Cadastro de aluno/professor
│ ├── cadastrar_disciplina_view.py # Cadastro de disciplinas
│ ├── cadastrar_aluno_disciplina_view.py # Associar aluno a disciplina
│ ├── trocar_senha_view.py # Alterar senha do usuário
│ └── remover_matricula_view.py # Remoção de aluno de uma disciplina
│
├── extensao.db # Banco de dados local (gerado automaticamente)
├── debug.txt # Logs de erro durante a execução
└── requirements.txt # Dependências do projeto



1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18

---

## 📋 Requisitos

### 🧰 Tecnologias Utilizadas

- **Python 3.6+**
- **Tkinter** (para interface gráfica)
- **SQLite** (para persistência de dados)
- **tkcalendar** (seleção de datas)
- **openpyxl** (exportação para Excel)
- **matplotlib/seaborn** (gráficos simples)

### 📦 Instale as dependências com:

```bash
pip install tkcalendar openpyxl matplotlib seaborn
Ou use o arquivo requirements.txt:

txt


1
2
3
4
tkcalendar >= 1.6.1
openpyxl >= 3.1.5
matplotlib >= 3.7.0
seaborn >= 0.12.0
🚀 Como Executar o Projeto
🔽 Clone o repositório:
bash


1
2
git clone https://github.com/DaviMattosDev/projeto-rad-python.git
cd projeto-rad-python
🧪 Instale as dependências:
bash


1
pip install -r requirements.txt
▶️ Execute o sistema:
bash


1
python main.py
Na primeira execução, o banco de dados será criado automaticamente (extensao.db).

🔒 Faça login como administrador:
Matrícula : admin
Senha : admin123
📊 Relatórios
A tela de relatórios permite:

Ver quantidade de alunos por disciplina
Ver média das notas por aluno/disciplina
Visualizar porcentagem de presenças
Exportar os dados em:
.csv
.xlsx (Excel)
📈 Gráficos Incluídos
Barras: Quantidade de alunos por turma
Histograma: Distribuição de notas
Gráfico de linhas: Frequência ao longo do tempo
📄 Licença
Este projeto está sob a licença MIT . Veja o arquivo LICENSE para mais detalhes.

👥 Colaboradores
NOME
FUNÇÃO
Davi Mattos
Desenvolvedor Principal

Se for grupo, adicione mais colaboradores aqui com links para seus perfis no GitHub. 

🤝 Contribuição
Contribuições são bem-vindas!

Como contribuir:
🍴 Fork do projeto
🔧 Crie um novo branch: git checkout -b feature/nova_funcionalidade
📥 Realize suas alterações
💾 Faça commit: git commit -m "Adiciona nova funcionalidade"
🚀 Envie para o GitHub: git push origin feature/nova_funcionalidade
📨 Abra um Pull Request no GitHub
💡 Melhorias Futuras
Futuramente, planejamos:

🔐 Criptografar senhas com hashlib
📄 Exportar relatórios em PDF
📅 Filtrar relatórios por período
📂 Histórico de operações realizadas no sistema
📁 Backup automático do banco de dados
📞 Entre em Contato
GitHub : DaviMattosDev
Instagram : @davimattosdev
Email : davimattos.contato@gmail.com
Projeto desenvolvido como Trabalho Prático de RAD – Entrega prevista para 06/06/2025 

Feito com ❤️ por Davi Mattos

