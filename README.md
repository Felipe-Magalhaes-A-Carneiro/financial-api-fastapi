# 💳 Financial API — FastAPI

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)](https://postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

API RESTful assíncrona para operações financeiras, desenvolvida como projeto de portfólio com foco em arquitetura, segurança e boas práticas de engenharia de software.

## ✨ Funcionalidades

- **Autenticação segura** via JWT (JSON Web Tokens)
- **Gerenciamento de contas** financeiras por usuário
- **Transações** com suporte a depósito, saque e transferência
- **Arquitetura assíncrona** de ponta a ponta com `asyncpg`
- **Migrations** controladas com Alembic
- **Testes automatizados** com pytest e pytest-asyncio
- **Containerização** completa com Docker e docker-compose

## 🏛️ Arquitetura

O projeto segue uma arquitetura em camadas inspirada em Domain-Driven Design (DDD) e Clean Architecture:

    ┌───────────────────────────────────────────────────────┐
    │ API Layer (FastAPI) │ ← Routers, validação de entrada │
    ├───────────────────────────────────────────────────────┤
    │ Service Layer │ ← Regras de negócio                   │
    ├───────────────────────────────────────────────────────┤
    │ Repository Layer │ ← Abstração do banco de dados      │ 
    ├───────────────────────────────────────────────────────┤
    │ Database Layer │ ← SQLAlchemy + PostgreSQL            │
    └───────────────────────────────────────────────────────┘


## 🚀 Início Rápido

### Pré-requisitos

- Python 3.12+
- PostgreSQL 16+
- Docker e docker-compose (opcional)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Felipe-Magalhaes-A-Carneiro/financial-api-fastapi.git
cd financial-api-fastapi

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instale as dependências
pip install -e ".[dev]"

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### Executando com Docker

```bash
docker-compose up --build
```

### Executando localmente

```bash
# Execute as migrations
alembic upgrade head

# Inicie o servidor de desenvolvimento
fastapi dev app/main.py
```

A documentação interativa estará disponível em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testes

```bash
pytest tests/ -v --asyncio-mode=auto
```

## 📁 Estrutura do Projeto

    financial-api-fastapi/
    ├── app/
    │ ├── api/v1/ # Endpoints e routers
    │ ├── core/ # Configurações, segurança, logging
    │ ├── db/ # Sessão e base do banco de dados
    │ ├── models/ # Models SQLAlchemy (ORM)
    │ ├── repositories/ # Camada de acesso a dados
    │ ├── schemas/ # Schemas Pydantic (validação)
    │ ├── services/ # Lógica de negócio
    │ └── main.py # Entry point
    ├── tests/ # Testes automatizados
    ├── alembic/ # Migrations
    ├── Dockerfile
    ├── docker-compose.yml
    └── pyproject.toml


## 🔒 Segurança

- Senhas armazenadas com hash `bcrypt`
- Autenticação stateless via JWT
- Variáveis sensíveis isoladas em `.env` (nunca versionadas)
- Rate limiting nos endpoints públicos

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) [em processo de finalização] para detalhes.
