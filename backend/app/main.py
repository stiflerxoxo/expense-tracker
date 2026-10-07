import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from .config import settings
from .database import Base, engine
from .routers import expenses

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("expense-tracker")


def init_db(retries: int = 15, delay: float = 2.0) -> None:
    """Create tables, waiting for Postgres to accept connections."""
    for attempt in range(1, retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            log.info("Database ready")
            return
        except Exception as exc:  # noqa: BLE001
            log.warning("DB not ready (%s/%s): %s", attempt, retries, exc.__class__.__name__)
            time.sleep(delay)
    raise RuntimeError("Could not connect to the database")


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Expense Tracker API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses.router)


@app.get("/api/health", tags=["health"])
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return {"status": "ok"}


# Local testing without Docker/nginx: set FRONTEND_DIR=../frontend to serve the UI from this app.
_frontend_dir = os.getenv("FRONTEND_DIR")
if _frontend_dir and os.path.isdir(_frontend_dir):
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")
