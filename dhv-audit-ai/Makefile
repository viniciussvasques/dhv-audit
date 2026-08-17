.PHONY: help install dev test lint typecheck coverage docker-up docker-down clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make install     — instala dependências Python"
	@echo "  make dev         — sobe API local (uvicorn)"
	@echo "  make test        — executa pytest"
	@echo "  make lint        — executa ruff"
	@echo "  make typecheck   — executa mypy"
	@echo "  make coverage    — pytest com cobertura"
	@echo "  make docker-up   — sobe PostgreSQL + API via Docker"
	@echo "  make docker-down — derruba containers"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

dev:
	uvicorn src.interfaces.api.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	ruff check src tests

typecheck:
	mypy src

coverage:
	pytest --cov=src --cov-report=term-missing

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/
