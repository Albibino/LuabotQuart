
# LuabotQuart API

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)[![Quart](https://img.shields.io/badge/Quart-006494?style=for-the-badge&logo=python&logoColor=white)](https://quart.palletsprojects.com/)[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)[![Alembic](https://img.shields.io/badge/Alembic-4E85A8?style=for-the-badge)](https://alembic.sqlalchemy.org/)

API backend para o projeto **LuaBot**, responsável por gerenciar todas as informações do banco de dados que alimentam o bot do Discord. O projeto foi desenvolvido utilizando uma arquitetura assíncrona com Python e Quart, seguindo os princípios da orientação a objetos.

**Desenvolvido por:** William Wollert T28

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Principais Tecnologias](#principais-tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração e Instalação](#configuração-e-instalação)
- [Gerenciamento do Banco de Dados (Alembic)](#gerenciamento-do-banco-de-dados-alembic)
## Sobre o Projeto

Este projeto serve como a espinha dorsal do **LuaBot**. Ele fornece uma interface RESTful para criar, ler, atualizar e deletar (CRUD) dados essenciais para o funcionamento do bot, como:

-   Informações de usuários do Discord.
-   Dados dos servidores (guildas) onde o bot está presente.
-   Sistema de níveis e XP dos usuários.
-   Registro de mensagens.
-   Upload e gerenciamento de fotos associadas aos usuários.
-   Logs da aplicação.

A API é construída com **Quart**, um framework web assíncrono compatível com a API do Flask, e utiliza **SQLAlchemy** com um driver `asyncpg` para se comunicar de forma não bloqueante com um banco de dados **PostgreSQL**.

## Principais Tecnologias

-   **Framework:** Quart
-   **Banco de Dados:** PostgreSQL
-   **ORM:** SQLAlchemy (com suporte assíncrono)
-   **Migrações de Schema:** Alembic
-   **Servidor ASGI:** Hypercorn (configurado via `run.py`)
-   **CORS:** Quart-CORS para permitir requisições de diferentes origens.

## Estrutura do Projeto

O projeto está organizado da seguinte forma para promover a separação de responsabilidades:

```
LuabotQuart/
├── app/
│   ├── controllers/    # Lógica de negócio (o que fazer com a requisição)
│   ├── models/         # Definição das tabelas do banco de dados (ORM)
│   ├── routes/         # Definição dos endpoints da API (as URLs)
│   ├── __init__.py     # Fábrica da aplicação Quart e configuração do DB
│   └── config.py       # Configurações da aplicação
├── migrations/         # Arquivos de migração do Alembic
├── alembic.ini         # Configuração do Alembic
├── requirements.txt    # Dependências do projeto
└── run.py              # Ponto de entrada para iniciar a aplicação
```

## Configuração e Instalação

Siga os passos abaixo para configurar e executar o projeto localmente.

### Pré-requisitos

-   Python 3.9+
-   PostgreSQL instalado e em execução.

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone "https://github.com/Albibino/LuabotQuart"
    cd LuabotQuart
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Linux / macOS
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados:**
    -   Crie um banco de dados no PostgreSQL chamado `luabotdb`.
    -   As credenciais de conexão estão definidas no arquivo `alembic.ini` e em `app/__init__.py`. Para um ambiente de produção, é recomendado usar variáveis de ambiente.
        ```ini
        # alembic.ini
        sqlalchemy.url = postgresql+asyncpg://postgres:postgres@localhost:5432/luabotdb
        ```

5.  **Execute as Migrações:**
    O Alembic gerenciará o schema do banco de dados. Para criar todas as tabelas, execute:
    ```bash
    alembic upgrade head
    ```

6.  **Inicie a aplicação:**
    ```bash
    python run.py
    ```
    A API estará disponível em `http://127.0.0.1:5000`.

## Gerenciamento do Banco de Dados (Alembic)

Qualquer alteração nos modelos em `app/models/` requer uma nova migração.

-   **Para gerar um novo arquivo de migração automaticamente:**
    ```bash
    alembic revision --autogenerate -m "Descrição da alteração"
    ```

-   **Para aplicar as migrações no banco de dados:**
    ```bash
    alembic upgrade head
    ```


