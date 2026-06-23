SHELL := /bin/sh

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(PYTHON) -m pip
RUFF := $(VENV)/bin/ruff
PYTEST := $(VENV)/bin/pytest
COMPOSE := docker compose --env-file .env -f infra/docker-compose.yml

.DEFAULT_GOAL := help

.PHONY: help setup install lint format test check up down logs

help: ## Show available commands.
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "%-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Create the local Python virtual environment.
	python3 -m venv $(VENV)
	@echo "Created $(VENV). Activate it manually with: source $(VENV)/bin/activate"

install: ## Install development dependencies into .venv.
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

lint: ## Run Ruff checks.
	$(RUFF) check .

format: ## Format Python files with Ruff.
	$(RUFF) format .

test: ## Run tests when they are present.
	@if find services -type f -name 'test_*.py' -print -quit | grep -q .; then \
		$(PYTEST); \
	else \
		echo "No tests are present yet."; \
	fi

check: lint test ## Run linting and tests.

up: ## Start local PostgreSQL and Redis.
	$(COMPOSE) up -d

down: ## Stop local infrastructure.
	$(COMPOSE) down

logs: ## Follow local infrastructure logs.
	$(COMPOSE) logs -f
