import os

os.environ["DATABASE_URL"] = "sqlite://"  # in-memory DB for unit tests

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


def override_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_db
client = TestClient(app)  # no context manager: skips startup DB wait


def make(**kw):
    body = {"title": "Coffee", "amount": 4.5, "category": "Food", "expense_date": "2026-01-15"}
    body.update(kw)
    return client.post("/api/expenses", json=body)


def test_create_and_get():
    r = make()
    assert r.status_code == 201
    eid = r.json()["id"]
    assert client.get(f"/api/expenses/{eid}").json()["title"] == "Coffee"


def test_validation_rejects_bad_amount():
    assert make(amount=-5).status_code == 422


def test_update_delete_404():
    eid = make().json()["id"]
    r = client.put(f"/api/expenses/{eid}", json={"title": "Tea", "amount": 3, "category": "Food", "expense_date": "2026-01-16"})
    assert r.json()["title"] == "Tea"
    assert client.delete(f"/api/expenses/{eid}").status_code == 204
    assert client.get(f"/api/expenses/{eid}").status_code == 404


def test_summary_and_filter():
    make(title="Bus", amount=2, category="Transport")
    s = client.get("/api/expenses/summary").json()
    assert s["count"] >= 1 and s["total"] > 0
    rows = client.get("/api/expenses?category=Transport").json()
    assert rows and all(x["category"] == "Transport" for x in rows)
