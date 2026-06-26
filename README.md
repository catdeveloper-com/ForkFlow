# ForkFlow

ForkFlow — учебный production-like микросервисный проект: социальная сеть для
разработчиков. Репозиторий развивается маленькими PR, чтобы постепенно
практиковать FastAPI, async Python, PostgreSQL, Redis, событийную интеграцию,
тестирование, наблюдаемость и чистую архитектуру.

## Текущий этап

Сейчас в репозитории есть общие инструменты разработки, локальные контейнеры
PostgreSQL и Redis, healthcheck Auth-сервиса, доменная модель регистрации и
application use case регистрации пользователя.

В проекте ещё нет HTTP endpoint регистрации, моделей базы данных, миграций,
JWT, хеширования паролей и реального хранилища пользователей.

`roadmap.pdf` — legacy-источник архитектурного материала. В нём может
встречаться старое имя проекта; во всех новых артефактах и документации
используется только ForkFlow.

## Требования

- Python 3.12+
- uv
- Docker Desktop с Docker Compose v2

## Быстрый старт

```bash
cp .env.example .env
make setup
make install
make up
make run-auth
```

`make setup` создаёт `.venv`. Если нужно запускать Python-команды напрямую,
активируй окружение вручную:

```bash
source .venv/bin/activate
```

Зависимости управляются через `uv`, а точные версии фиксируются в `uv.lock`.

## Частые команды

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

## Локальная инфраструктура

`infra/docker-compose.yml` запускает только зависимости, нужные для первых
этапов проекта:

- PostgreSQL: будущий source of truth для данных сервисов;
- Redis: disposable cache и хранилище временного состояния.

Kafka, RabbitMQ, Celery, gateway, monitoring и дополнительные сервисы
осознанно отложены до конкретного продуктового сценария.

## Структура репозитория

```text
ForkFlow/
├── infra/              # Локальная инфраструктура разработки
├── services/auth/      # Auth-сервис
├── .env.example        # Безопасный шаблон локальной конфигурации
├── Makefile            # Общие команды разработки
├── pyproject.toml      # Метаданные проекта, зависимости, Ruff и pytest
└── uv.lock             # Lockfile зависимостей
```

## Следующий этап

Следующий сфокусированный шаг после перехода на `uv` — продолжить Auth
регистрацию: добавить пароль и хеширование либо подготовить infrastructure
слой для PostgreSQL. Эти изменения должны идти отдельными PR.
