# Aura Skincare

Aura Skincare is a modular monolith platform built with FastAPI, SQLAlchemy, and Docker Compose.

## Getting Started

1. Copy `backend/.env.example` to `backend/.env` and fill in real values.
2. Start services: `docker compose up --build`
3. Run database migrations: `docker compose exec backend alembic upgrade head`
4. Access API docs: http://localhost:8000/docs
5. Health check: http://localhost:8000/health

## Scripts

- `make install` - Install dependencies
- `make dev` - Start development server
- `make test` - Run tests
- `make lint` - Run linter
- `make format` - Format code
- `make clean` - Clean caches
- `make docker-up` - Start Docker Compose
- `make docker-down` - Stop Docker Compose

## Documentation

See `Aura-Skincare-Docs/` for requirements, architecture, and API specifications.
