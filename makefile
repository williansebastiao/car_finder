SHELL := /bin/bash
.DEFAULT_GOAL := help
DOCKER_COMPOSE := docker-compose
POETRY_CMD := poetry run

.PHONY: help scaffold alembic start build stop migration migrate seed lint tests run

help:
	@echo "Car Finder - Makefile"
	@echo "---------------------"
	@echo "Usage: make <command>"
	@echo ""
	@echo "Commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-26s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

scaffold: ## Start config to project
	@if [ ! -e .env ]; then \
		cp .env.example .env; \
	fi
	poetry update

alembic: ## Start alembic
	$(POETRY_CMD) alembic init -t async migrations

start: ## Start all containers
	$(DOCKER_COMPOSE) up -d

build: ## Build all containers without detach
	$(DOCKER_COMPOSE) up --build

stop: ## Stop all containers
	$(DOCKER_COMPOSE) down --remove-orphans

migration: ## Create a migration
	$(DOCKER) $(POETRY_CMD) alembic revision --autogenerate -m "$(message)"

migrate: ## Run migration
	$(DOCKER) $(POETRY_CMD) alembic upgrade head

seed: ## Insert fake vehicles into the database (requires DB running + migrated)
	$(POETRY_CMD) python -m src.database.seed.vehicle

run: ## Start the Car Finder terminal agent
	$(POETRY_CMD) python -m src.main

lint: ## Run all linting tools
	$(POETRY_CMD) ruff check --fix
	$(POETRY_CMD) ruff format

tests: ## Run Pytest inside the Docker container
	$(POETRY_CMD) pytest --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80 --cov-config=pyproject.toml .
