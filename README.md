# Expense Tracker

A basic full-stack expense tracker built as a DevOps practice project.

| Layer    | Tech                              |
|----------|-----------------------------------|
| Frontend | HTML / CSS / vanilla JS, served by Nginx (also reverse-proxies `/api`) |
| Backend  | Python 3.12, FastAPI, SQLAlchemy  |
| Database | PostgreSQL 16                     |
| Runtime  | Docker + Docker Compose           |

## Project structure

```
expense-tracker/
├── backend/                 # FastAPI service
│   ├── app/
│   │   ├── main.py          # app entrypoint, health check, DB init
│   │   ├── config.py        # env-based settings
│   │   ├── database.py      # engine / session
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── routers/expenses.py
│   ├── tests/               # pytest unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # static UI + nginx
│   ├── index.html, css/, js/
│   ├── nginx.conf
│   └── Dockerfile
├── database/init.sql        # reference schema (runs on first DB start)
├── docker-compose.yml
├── .env.example
├── Makefile
└── README.md
```

## Run it

```bash
cp .env.example .env        # then change POSTGRES_PASSWORD
docker compose up -d --build
```

Open http://localhost:8080 — health check: http://localhost:8080/api/health

Stop: `docker compose down` (add `-v` to delete the database volume).

## API

| Method | Path                    | Description            |
|--------|-------------------------|------------------------|
| GET    | `/api/health`           | App + DB health        |
| GET    | `/api/expenses`         | List (`?category=`)    |
| POST   | `/api/expenses`         | Create                 |
| GET    | `/api/expenses/{id}`    | Get one                |
| PUT    | `/api/expenses/{id}`    | Update                 |
| DELETE | `/api/expenses/{id}`    | Delete                 |
| GET    | `/api/expenses/summary` | Totals by category     |

## Tests

```bash
cd backend && pip install -r requirements.txt && pytest -q
```

## Configuration

All settings come from environment variables (see `.env.example`). Never commit `.env`.

## Quick test without Docker (Python only)

Uses a temporary SQLite file instead of Postgres. Run from the `backend` folder, with Python 3.10+.

```bash
python -m venv .venv
# Mac/Linux: source .venv/bin/activate     Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Mac/Linux:
```bash
DATABASE_URL=sqlite:///./test.db FRONTEND_DIR=../frontend python -m uvicorn app.main:app --port 8000
```

Windows PowerShell:
```powershell
$env:DATABASE_URL="sqlite:///./test.db"
$env:FRONTEND_DIR="../frontend"
python -m uvicorn app.main:app --port 8000
```

Open http://localhost:8000
