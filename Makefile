SHELL := /bin/sh

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip
RUFF := $(VENV)/bin/ruff
PYTEST := $(VENV)/bin/pytest
COMPOSE := docker compose --env-file .env -f infra/docker-compose.yml
AUTH_MODULE := services.auth.app.main:app

.DEFAULT_GOAL := help

.PHONY: help setup install lint format test check up down logs run-auth

help: ## Показать доступные команды.
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "%-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Создать локальное Python-виртуальное окружение.
	python3 -m venv $(VENV)
	@echo "Создано $(VENV). Активируй окружение вручную: source $(VENV)/bin/activate"

install: ## Установить зависимости для разработки в .venv.
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

lint: ## Запустить проверки Ruff.
	$(RUFF) check .

format: ## Отформатировать Python-файлы через Ruff.
	$(RUFF) format .

test: ## Запустить тесты, если они есть.
	@if find services -type f -name 'test_*.py' -print -quit | grep -q .; then \
		$(PYTEST); \
	else \
		echo "Тестов пока нет."; \
	fi

check: lint test ## Запустить линтер и тесты.

up: ## Запустить локальные PostgreSQL и Redis.
	$(COMPOSE) up -d

down: ## Остановить локальную инфраструктуру.
	$(COMPOSE) down

logs: ## Читать логи локальной инфраструктуры.
	$(COMPOSE) logs -f

run-auth: ## Запустить health-check endpoint Auth-сервиса на порту 8000.
	$(PYTHON) -m uvicorn $(AUTH_MODULE) --port 8000
