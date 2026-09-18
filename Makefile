.PHONY: help install dev test lint format clean docker-up docker-down

help:
	@echo "Aura Skincare Backend Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  install      Install dependencies"
	@echo "  dev          Start development server"
	@echo "  test         Run tests"
	@echo "  lint         Run linting"
	@echo "  format       Format code"
	@echo "  clean        Clean cache and build artifacts"
	@echo "  docker-up    Start Docker Compose services"
	@echo "  docker-down  Stop Docker Compose services"

install:
	uv sync

dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check .
	uv run mypy .

format:
	uv run ruff format .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache .ruff_cache .pytest_cache .coverage htmlcov

docker-up:
	docker compose up --build

docker-down:
	docker compose down
