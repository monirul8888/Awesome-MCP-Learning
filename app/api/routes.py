from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ExpenseCreate, ExpenseResponse, ExpenseSummary
from app import crud
from typing import Optional

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse, status_code=201)
def add_expense(data: ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, data)

@router.get("/", response_model=ExpenseSummary)
def list_expenses(
    category : Optional[str] = Query(None),
    month    : Optional[int] = Query(None, ge=1, le=12),
    year     : Optional[int] = Query(None, ge=2000),
    limit    : int           = Query(50, ge=1, le=200),
    db       : Session       = Depends(get_db),
):
    expenses, total = crud.get_expenses(db, category, month, year, limit)
    return ExpenseSummary(
        total    = total,
        count    = len(expenses),
        expenses = expenses,
    )