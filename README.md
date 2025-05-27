# 🎓 Sistema de Gerenciamento de Extensão Universitária

![GitHub repo size](https://img.shields.io/github/repo-size/DaviMattosDev/projeto-rad-python?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/DaviMattosDev/projeto-rad-python?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/DaviMattosDev/projeto-rad-python?color=blue&style=for-the-badge)

> Projeto acadêmico desenvolvido como parte do Trabalho Prático da disciplina de RAD (Rapid Application Development).

Este sistema permite ao administrador, professores e alunos realizar diversas ações no gerenciamento univesitário, como:

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
| **Desmatricular Aluno ou Professor** | Desmatricula um Aluno ou Professor |

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
│   └── desmatricular_model.py
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
│   └── desmatricular_view.py
│
├── extensao.db
├── debug_db.txt
├── debug.txt
└── requirements.txt
```

---

## 📋 Instalação

```bash
git clone https://github.com/DaviMattosDev/projeto-rad-python.git
cd projeto-rad-python
```

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
python database/db.py
python main.py

python testes/criar_usuarios_exemplo.py (caso queira criar usuários de teste automaticamente)
```

Na primeira execução, o banco de dados `extensao.db` será criado automaticamente.

### 🔒 Login Administrador padrão

- Matrícula: `123`
- Senha: `admin123`

---

### 🔐 Login Aluno ou Professor após cadastro

Após cadastrar um novo **Aluno** ou **Professor**, o sistema gera automaticamente uma **matrícula única** e uma **senha padrão inicial** para o primeiro acesso.


### 📌 Como funciona:

- A **matrícula** é gerada automaticamente com a função `gerar_matricula()`, normalmente combinando o ano atual com um número aleatório.  
  **Exemplo:** `20251234`

- A **senha padrão** é gerada com base nos **últimos 3 dígitos do CPF** e na **data de nascimento** do usuário.  
  Isso é feito com a função `gerar_senha_padrao(data_nascimento, cpf)`.


### 🧪 Exemplo prático

Suponha que um aluno tenha os seguintes dados:

- CPF: `123.456.789-09`
- Data de nascimento: `15/08/2004`

A **senha padrão** gerada seria:

- Data de nascimento sem barras: `15082004`
- Últimos 3 dígitos do CPF: `909`

**Senha padrão inicial:** `15082004909`


### 🆔 Login gerado após cadastro:

- Matrícula: *(gerada automaticamente, ex:)* `20253782`
- Senha: `15082004909` *(baseada no CPF e data de nascimento)*

> ⚠️ **Importante:** essa senha é **temporária** e deve ser alterada no primeiro acesso para garantir a segurança da conta.

---

---

## 📋 Tela do Aluno

Após o login, o aluno acessa uma interface dividida em três áreas principais:

### 1. 📘 Disciplinas Cursadas  
- Exibe disciplinas com:
  - Nome da disciplina  
  - Professor responsável  
  - Frequência (%): destaca em **vermelho** se < 50%  
  - Nota final: valor numérico ou "N/A"

### 2. 📅 Próximas Avaliações  
- Lista avaliações futuras com:
  - Nome da disciplina  
  - Data  
  - Descrição  
  - Tipo (AV1, AV2, AVS)

### 3. 📊 Notas por Prova  
- Mostra notas lançadas pelo professor organizadas por tipo de avaliação  
- Se não houver nota, exibe como "N/A"

### 🔧 Ações Disponíveis
- `Trocar Senha`: abre tela de alteração de senha  
- `Logout`: encerra sessão e retorna à tela de login

---

## 👨‍🏫 Tela do Professor

O professor tem acesso a uma interface com **três abas**:

### 1. 🧭 Marcar Presença  
- Exibe lista de alunos com status:
  - Presente (**verde**)  
  - Ausente (**vermelho**)  
- Botões:
  - `Confirmar Presença`  
  - `Marcar Falta`

### 2. 📝 Lançar Notas  
Campos:
- Selecionar aluno  
- Tipo de avaliação (AV1, AV2, AVS)  
- Digitar nota (0.0–10.0) ou marcar “Falta”

Botão:
- `Salvar Nota` → registra os dados no sistema

> ⚠️ Validação automática de valores entre 0.0 e 10.0.

### 3. 🧾 Avaliações  
Duas partes:

#### 🔧 Criar Nova Avaliação  
Campos:
- Selecionar disciplina  
- Descrição  
- Data (via calendário)  
- Tipo (AV1, AV2, AVS)  
Botão:
- `Criar Avaliação`

#### 📋 Avaliações Criadas  
Exibe:
- Disciplina  
- Data  
- Descrição  
- Tipo  
- Nº de alunos aprovados  
- Nº de faltas

---

## 👤 Tela do Administrador

Interface centralizada para gerenciamento do sistema com botões que levam às funcionalidades abaixo:

### 🔘 Funções Disponíveis:

| Botão | Descrição |
|-------|-----------|
| **Cadastrar Aluno** | Abre tela para cadastrar um novo aluno |
| **Cadastrar Professor** | Abre tela para cadastrar um novo professor |
| **Cadastrar Disciplina** | Abre tela para criar nova disciplina |
| **Cadastrar Aluno em Disciplina** | Vincula aluno a uma disciplina |
| **Desmatricular Aluno ou Professor** | Abre uma tela para desmatricular um aluno ou professor da universidade |
| **Relatórios** | Gera relatórios acadêmicos gerais |
| **Remover Aluno de Professor** | Desvincula aluno de um professor |
| **Trocar Senha** | Abre tela de alteração de senha |
| **Deslogar** | Encerra sessão e volta à tela de login |

> ✅ Todas as telas são abertas em janelas separadas e centralizadas na tela principal.

---

## 🔐 Troca de Senha (comum para todos os perfis)

Tela com os campos:
- Senha Atual  
- Nova Senha  
- Confirmação da Nova Senha  

Botão:
- `Salvar` → redireciona para a tela principal após sucesso

---

## 🚪 Logout (comum para todos os perfis)

Ação:
- Fecha a janela atual  
- Retorna à tela de login

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

> (grupo).

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
- Linkedin: [Davi Mattos](https://www.linkedin.com/in/davi-mattos-5a39b3288)
- Email: [Davirjti@gmail.com](mailto:davirjti@gmail.com)

> Projeto desenvolvido como Trabalho Prático de RAD – Entrega prevista para **06/06/2025**

---

Feito com ❤️ por **Davi Mattos**
