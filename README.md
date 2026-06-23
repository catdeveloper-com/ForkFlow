# ForkFlow

ForkFlow is an educational, production-like microservice social network for
developers. The repository is being built incrementally to demonstrate
maintainable FastAPI services, asynchronous Python, PostgreSQL, Redis,
event-driven integration, testing, and observability.

## Current stage

This foundation stage provides shared developer tooling and local PostgreSQL
and Redis containers. It intentionally contains no application services,
HTTP endpoints, database models, migrations, or business logic.

`roadmap.pdf` is a legacy architectural source. It may retain a historic
project name; ForkFlow is the only current project name for repository
artifacts and documentation.

## Prerequisites

- Python 3.12+
- Docker Desktop with Docker Compose v2

## Quick start

```bash
cp .env.example .env
make setup
make install
make up
```

`make setup` creates `.venv`; activate it manually in your shell if you need
to run Python commands directly:

```bash
source .venv/bin/activate
```

## Common commands

```bash
make help
make lint
make format
make test
make check
make up
make down
make logs
```

## Local infrastructure

`infra/docker-compose.yml` starts only the dependencies required by the first
service milestones:

- PostgreSQL: the future source of truth for service-owned data;
- Redis: a disposable cache and temporary-state store.

Kafka, RabbitMQ, Celery, gateway, monitoring, and additional services are
deliberately deferred until a concrete product scenario requires them.

## Repository layout

```text
ForkFlow/
├── infra/              # Local development infrastructure
├── services/
│   └── auth/           # Documentation for the future Auth service boundary
├── .env.example        # Safe local configuration template
├── Makefile            # Shared developer commands
├── pyproject.toml      # Ruff and pytest configuration
└── requirements-dev.txt
```

## Next milestone

The next focused change can introduce an executable Auth service skeleton with
a health check and its first tests. Registration, credentials, tokens, data
models, and migrations remain outside this foundation stage.
