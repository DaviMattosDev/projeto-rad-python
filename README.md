# 🎓 Sistema de Gerenciamento Escolar

![GitHub repo size](https://img.shields.io/github/repo-size/DaviMattosDev/projeto-rad-python?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/DaviMattosDev/projeto-rad-python?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/DaviMattosDev/projeto-rad-python?color=blue&style=for-the-badge)

> Projeto acadêmico desenvolvido como parte do Trabalho Prático da disciplina de RAD (Rapid Application Development).

Este sistema permite ao administrador, professores e alunos realizar diversas ações no gerenciamento escolar, como:

- 🔐 Login com validação por matrícula e senha  
- 👥 Cadastro de Aluno e Professor com criptografia hash  
- 📘 Cadastrar Disciplina e associar ao professor  
- 🧾 Associar aluno a uma disciplina  
- 📋 Registrar presença/falta dos alunos  
- 📊 Lançar notas das avaliações (AV1, AV2, AVS)  
- ❌ Remover aluno de uma disciplina  
- 📈 Relatórios visuais com gráficos e exportação para CSV/Excel  

## 💻 Tecnologias Utilizadas

- Python 3.6+
- Tkinter (GUI)
- SQLite (banco local)
- tkcalendar (datas)
- openpyxl (Excel)
- matplotlib / seaborn (gráficos)

---

## 🧩 Funcionalidades Implementadas

| Módulo | Descrição |
|--------|----------|
| **Login** | Tela inicial de autenticação com validação de matrícula e senha |
| **Cadastro de Usuários** | Permite cadastrar novos alunos e professores |
| **Cadastro de Disciplinas** | Associa disciplinas a professores |
| **Matricular Aluno em Disciplina** | Vincula aluno à uma disciplina ministrada por um professor |
| **Marcar Presença/Falta** | Registra presença dos alunos em aulas |
| **Lançar Notas** | Registra AV1, AV2, AVS e marca falta se necessário |
| **Remover Aluno de Professor** | Desvincula aluno de sua disciplina atual |
| **Relatórios Visuais** | Exibe gráficos de frequência e desempenho |
| **Exportação de Dados** | Gera relatórios em CSV e Excel |

---

## 🗃️ Banco de Dados SQLite (`extensao.db`)

### `usuarios`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| nome_completo | TEXT | Nome do usuário |
| email | TEXT | Email único |
| senha | TEXT | Senha (texto plano) |
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
| professor_id | INTEGER | ID do professor |

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

```
projeto-rad-python/
│
├── controllers/
│   └── auth_controller.py
│
├── database/
│   └── db.py
│
│
├── utils/
│   └── helpers.py
│
│
├── models/
│   ├── usuario.py
│   ├── disciplina.py
│   ├── aluno_model.py
│   └── remover_aluno_professor_model.py
│   └── professor.py
│   └── aluno.py
│   └── aluno_disciplina.py
│
│
├── views/
│   ├── login_view.py
│   ├── admin_view.py
│   ├── professor_view.py
│   ├── aluno_view.py
│   ├── relatorios_view.py
│   ├── cadastrar_usuario_view.py
│   ├── cadastrar_disciplina_view.py
│   ├── cadastrar_aluno_disciplina_view.py
│   ├── trocar_senha_view.py
│   └── remover_matricula_view.py
│
│
├── extensao.db
├── debug_db.txt
├── debug.txt
└── requirements.txt
```

---

## 📋 Instalação

### 📦 Instale as dependências com:

```bash
pip install tkcalendar openpyxl matplotlib seaborn
```

Ou use o `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Executar o Projeto

```bash
git clone https://github.com/DaviMattosDev/projeto-rad-python.git
cd projeto-rad-python
python database/db.py
python main.py

python testes/criar_usuarios_exemplo.py (caso queira criar usuários de teste automaticamente)
```

Na primeira execução, o banco de dados `extensao.db` será criado automaticamente.

### 🔒 Login padrão

- Matrícula: `123`
- Senha: `admin123`

---

## 📊 Relatórios

- Quantidade de alunos por disciplina
- Média de notas por aluno/disciplina
- Porcentagem de presenças

### Exportações

- `.csv`
- `.xlsx (Excel)`

### Gráficos

- 📊 Barras: Alunos por turma
- 📉 Histograma: Notas
- 📈 Linhas: Frequência por tempo

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👥 Colaboradores

- **Davi Mattos** — Desenvolvedor Principal

> Se for grupo, adicione mais nomes aqui com links para os perfis do GitHub.

---

## 🤝 Contribuição

Contribuições são bem-vindas!

Como contribuir:

1. 🍴 Fork do projeto  
2. 🔧 Crie um branch: `git checkout -b feature/nova_funcionalidade`  
3. 💾 Commit: `git commit -m "Adiciona nova funcionalidade"`  
4. 🚀 Push: `git push origin feature/nova_funcionalidade`  
5. 📨 Abra um Pull Request

---

## 💡 Melhorias Futuras

- 📄 Exportar relatórios em PDF
- 📅 Filtros por período nos relatórios
- 📂 Histórico de ações
- 📁 Backup automático do banco de dados

---

## 📞 Contato

- GitHub: [DaviMattosDev](https://github.com/DaviMattosDev)
- Instagram: [@davimattosdev](https://instagram.com/davimattosdev)
- Email: [davimattos.contato@gmail.com](mailto:davimattos.contato@gmail.com)

> Projeto desenvolvido como Trabalho Prático de RAD – Entrega prevista para **06/06/2025**

---

Feito com ❤️ por **Davi Mattos**
