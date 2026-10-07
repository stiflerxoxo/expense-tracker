from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.get("", response_model=list[schemas.ExpenseOut])
def list_expenses(
    category: str | None = None,
    limit: int = Query(200, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    stmt = select(models.Expense).order_by(
        models.Expense.expense_date.desc(), models.Expense.id.desc()
    )
    if category:
        stmt = stmt.where(models.Expense.category == category)
    return db.scalars(stmt.limit(limit)).all()


@router.get("/summary", response_model=schemas.Summary)
def summary(db: Session = Depends(get_db)):
    rows = db.execute(
        select(models.Expense.category, func.sum(models.Expense.amount))
        .group_by(models.Expense.category)
        .order_by(func.sum(models.Expense.amount).desc())
    ).all()
    count = db.scalar(select(func.count(models.Expense.id))) or 0
    by_category = [{"category": c, "total": float(t)} for c, t in rows]
    return {"total": sum(r["total"] for r in by_category), "count": count, "by_category": by_category}


@router.post("", response_model=schemas.ExpenseOut, status_code=status.HTTP_201_CREATED)
def create_expense(payload: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    expense = models.Expense(**payload.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def _get_or_404(db: Session, expense_id: int) -> models.Expense:
    expense = db.get(models.Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.get("/{expense_id}", response_model=schemas.ExpenseOut)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, expense_id)


@router.put("/{expense_id}", response_model=schemas.ExpenseOut)
def update_expense(expense_id: int, payload: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    expense = _get_or_404(db, expense_id)
    for key, value in payload.model_dump().items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db.delete(_get_or_404(db, expense_id))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
