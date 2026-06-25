# ForkFlow

ForkFlow is an educational, production-like microservice social network for
developers. The repository is being built incrementally to demonstrate
maintainable FastAPI services, asynchronous Python, PostgreSQL, Redis,
event-driven integration, testing, and observability.

## Current stage

This stage provides shared developer tooling, local PostgreSQL and Redis
containers, and an executable Auth service health check. It intentionally
contains no business endpoints, database models, migrations, or authentication
flows.

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
make run-auth
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
make run-auth
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
├── services/auth/      # Auth service health-check skeleton and documentation
├── .env.example        # Safe local configuration template
├── Makefile            # Shared developer commands
├── pyproject.toml      # Ruff and pytest configuration
└── requirements-dev.txt
```

## Next milestone

The next focused change can introduce Auth configuration and persistence.
Registration, credentials, tokens, data models, and migrations remain outside
the current scope.
