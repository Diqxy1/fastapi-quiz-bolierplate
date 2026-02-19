# 🏆 Quiz API - Ranking & Gamification System

Este projeto é uma API de Quiz para estudo desenvolvida com **FastAPI** e **SQLAlchemy**

## 🚀 Funcionalidades implementadas

- **Ranking Global:** Ordenação automática por pontuação acumulada.
- **Ranking por Categoria:** Filtro de performance individual por tema.
- **Sistema de Gamificação:** - Acerto: `+1` ponto.
  - Erro: `-1` ponto (com trava de segurança para nunca ficar negativo).
- **Arquitetura Sólida:** Separação clara entre Entities (DB) e Models (Pydantic).
- **Consistência de Dados:** Uso de `refresh_total_score` para sincronizar o saldo global com as categorias.

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Web framework de alta performance.
- **SQLAlchemy 2.0**: Mapeamento objeto-relacional (ORM) com suporte assíncrono.
- **Alembic**: Controle de versionamento de banco de dados (Migrations manuais).
- **PostgreSQL**: Banco de dados relacional.
- **Pydantic**: Validação de dados e schemas.

## 📊 Estrutura do Banco de Dados

O sistema utiliza três tabelas principais para a lógica de pontos:
1. `users`: Armazena o `total_score` acumulado.
2. `categories`: Define os temas das perguntas.
3. `user_category_scores`: Tabela pivô que guarda o desempenho de cada usuário por categoria.

## 📥 Instalação e Migrations

-   Criar nova migration:


```bash
alembic -c migrations/alembic.ini revision -m "descrição"
```

-   Aplicar migrations:

```bash
alembic -c migrations/alembic.ini upgrade head
```

-   Ver histórico:

```bash
alembic -c migrations/alembic.ini history
```