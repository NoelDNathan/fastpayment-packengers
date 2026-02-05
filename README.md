# Fastpayment API

FastAPI backend for Fastpayment, using SQLAlchemy (async) and Pydantic.

## Requirements

- Docker and Docker Compose

## Quick Start with Docker

### 1. Create environment file

Ensure `.env.dev` exists (copy from `.env.example` if needed):

```bash
cp .env.example .env.dev
```

### 2. Build and start services

```bash
cd fastpayment
docker compose -f docker-compose.dev.yml up --build -d
```

### 3. Run migrations

```bash
docker compose -f docker-compose.dev.yml exec api alembic upgrade head
```

### 4. Verify

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Useful commands

| Command | Description |
|---------|-------------|
| `docker compose -f docker-compose.dev.yml up -d` | Start services in background |
| `docker compose -f docker-compose.dev.yml down` | Stop services |
| `docker compose -f docker-compose.dev.yml logs -f api` | View API logs |
| `docker compose -f docker-compose.dev.yml exec api alembic upgrade head` | Run migrations |
| `docker compose -f docker-compose.dev.yml exec api alembic revision --autogenerate -m "description"` | Create new migration |

## Local development (without Docker)

1. Create a Python virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. Start Postgres (or use Docker for DB only):

   ```bash
   docker run -d --name fastpayment-db -e POSTGRES_USER=fastpayment -e POSTGRES_PASSWORD=fastpayment -e POSTGRES_DB=fastpayment_dev -p 5433:5432 postgres:15-alpine
   ```

3. Set `DATABASE_URL=postgresql+asyncpg://fastpayment:fastpayment@localhost:5433/fastpayment_dev` in `.env`

4. Run migrations and start the API:

   ```bash
   alembic upgrade head
   uvicorn app.main:app --reload --port 8000
   ```

## Project structure

```
fastpayment/
├── app/
│   ├── main.py          # FastAPI app
│   ├── config.py        # Settings (Pydantic)
│   ├── database.py      # SQLAlchemy async setup
│   ├── dependencies.py
│   ├── middleware.py
│   ├── models/          # SQLAlchemy models
│   ├── routers/
│   ├── schemas/         # Pydantic schemas
│   └── utils/
├── alembic/             # Migrations
├── docker/
├── docker-compose.dev.yml
├── requirements.txt
└── README.md
```
