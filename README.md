---

# 🚀 Projeto RAD Python

![GitHub repo size](https://img.shields.io/github/repo-size/DaviMattosDev/projeto-rad-python?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/DaviMattosDev/projeto-rad-python?style=for-the-badge)
![GitHub commits](https://img.shields.io/github/commit-activity/t/DaviMattosDev/projeto-rad-python?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/DaviMattosDev/projeto-rad-python?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/DaviMattosDev/projeto-rad-python?style=for-the-badge)

<img src="imagem.png" alt="Logo do Projeto">

> O **Projeto RAD Python** é uma aplicação desenvolvida para demonstrar práticas de desenvolvimento ágil e eficiente em Python. Ele foi projetado para ser modular, fácil de usar e extensível.

---

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Estrutura dos Scripts](#estrutura-dos-scripts)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
  - [Gerenciamento de Departamento (`gerenciador_departamentos.py`)](#gerenciamento-de-departamentospy)
  - [Script Principal (`main.py`)](#mainpy)
  - [Login (`login_utils.py`)](#login_utilspy)
  - [Gerenciamento de Funcionários (`funcionarios.py`)](#gerenciamento-de-frequênciapy)
  - [Frequência de funcionario (`frequencia_funcionario.py`)](#frequencia-funcionariopy)
- [Contribuição](#contribuição)
- [Colaboradores](#colaboradores)
- [Licença](#licença)

---

## 🌟 Sobre o Projeto

O **Projeto RAD Python** é uma aplicação desktop desenvolvida com Python e Tkinter, integrada a um banco de dados SQLite. Ele permite gerenciar funcionários e suas frequências, além de gerar relatórios detalhados sobre salários e horas trabalhadas. Este projeto é ideal para quem deseja aprender ou implementar práticas de desenvolvimento ágil (RAD) em Python.

---

## 📂 Estrutura dos Scripts

O projeto é composto por:

1. **`main.py`**: Script principal que contém a interface gráfica e a lógica do sistema.
2. **`login_utils.py`**: Módulo responsável pela autenticação de usuários.
3. **`frequencia_funcionario.py`**: Módulo para funcionários e interações com o banco de dados.
4. **`gerenciador_departamentos.py`**: Módulo para manutenção de departamento e interações com o banco de dados.
5. **`gerenciador_frequencia.py`**: Módulo para manutenção de funcionários e interações com o banco de dados.
6. **`criar_banco.py`**: Script principal da criação do banco de dados.

---

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- **Python 3.x**: Certifique-se de ter instalado a versão mais recente do Python. Verifique com:
  ```bash
  python --version
  ```
  Ou, dependendo da sua configuração:
  ```bash
  python3 --version
  ```

- **Dependências**: Instale as bibliotecas necessárias usando o `pip`:
  ```bash
  pip install tkinter sqlite3 tkcalendar
  ```

- **Banco de Dados SQLite**: O arquivo `empresa.db` será criado automaticamente ao executar o sistema pela primeira vez. Certifique-se de que a pasta do projeto tenha permissão de escrita.

---

## 🚀 Instalação

Para instalar e configurar o **Projeto RAD Python**, siga estas etapas:

### Clonando o Repositório
```bash
git clone https://github.com/DaviMattosDev/projeto-rad-python.git
cd projeto-rad-python
```

### Instalando Dependências
```bash
pip install -r requirements.txt
```

### Executando o Sistema
Execute o script principal:
```bash
python main.py
```

---

## ☕ Como Usar

### **Script Principal (`main.py`)**
Este é o coração do sistema, onde a interface gráfica e a lógica principal estão implementadas.

#### Funcionalidades:
- **Alterar Status de Frequência**:
  - Insira o **ID do Funcionário** no campo correspondente.
  - Selecione o **Novo Status** no menu suspenso (`pendente`, `confirmado`, `nao_confirmado`).
  - Clique no botão **Alterar Status** para atualizar o status no banco de dados.

- **Gerar Relatório de Salário**:
  - Clique no botão **Gerar Relatório de Salário**.
  - Um arquivo chamado `relatorio_salario.txt` será criado na mesma pasta do script.
  - O relatório inclui informações como nome do funcionário, dias trabalhados, horas totais e status de pagamento.

- **Listar Frequência**:
  - Clique no botão **Listar Frequência** para exibir todos os registros na tabela.
  - A tabela exibe informações como ID, Funcionário ID, Entrada, Saída, Tipo e Status (com cores indicando o estado).

#### Navegação:
- Use a **barra de rolagem vertical** à direita para navegar pelo conteúdo, caso ele ultrapasse o espaço visível.

---

### **Login (`login_utils.py`)**
Este módulo é responsável pela autenticação de usuários.

#### Como Funciona:
- O sistema verifica as credenciais inseridas na janela de login.
- Exemplo de credenciais válidas:
  - **Usuário**: admin
  - **Senha**: 12345

#### Personalização:
- Você pode adicionar novos usuários e senhas diretamente no código ou implementar um sistema de cadastro de usuários no futuro.

---

### **Gerenciamento de Funcionários (`funcionarios.py`)**
Este módulo gerencia as operações relacionadas aos funcionários e ao banco de dados.

#### Funcionalidades:
- **Cadastro de Funcionários**:
  - Insira o nome, cargo, departamento, situação e data de início.
  - Clique no botão **Cadastrar** para salvar os dados no banco de dados.

- **Atualização/Exclusão de Funcionários**:
  - Insira o **ID do Funcionário** e selecione o campo a ser atualizado.
  - Informe o novo valor e clique em **Atualizar** ou **Excluir**.

#### Banco de Dados:
- O módulo interage diretamente com o banco de dados SQLite (`empresa.db`) para realizar operações CRUD (Create, Read, Update, Delete).

---

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir com o **Projeto RAD Python**, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`.
4. Envie para o branch original: `git push origin projeto-rad-python/<local>`.
5. Crie a solicitação de pull.

Consulte a [documentação oficial do GitHub](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) para mais detalhes.

---

## 🙌 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/DaviMattosDev" title="Davi Mattos">
        <img src="https://avatars.githubusercontent.com/DaviMattosDev" width="100px;" alt="Foto do Davi Mattos no GitHub"/><br>
        <sub>
          <b>Davi Mattos</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

---

## 😄 Seja um dos Contribuidores

Quer fazer parte desse projeto? Leia o guia de contribuição em [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.

---

