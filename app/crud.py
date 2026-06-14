from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from app.models import Expense
from app.schemas import ExpenseCreate
from datetime import date
from decimal import Decimal
from typing import Optional

def create_expense(db: Session, data: ExpenseCreate) -> Expense:
    expense = Expense(
        amount      = data.amount,
        category    = data.category.strip().title(),
        description = data.description.strip() if data.description else None,
        date        = data.date or date.today(),
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_expenses(
    db       : Session,
    category : Optional[str] = None,
    month    : Optional[int] = None,
    year     : Optional[int] = None,
    limit    : int = 50,
) -> tuple[list[Expense], Decimal]:

    query = db.query(Expense)

    if category:
        query = query.filter(func.lower(Expense.category) == category.lower())
    if month:
        query = query.filter(extract("month", Expense.date) == month)
    if year:
        query = query.filter(extract("year", Expense.date) == year)

    expenses = query.order_by(Expense.date.desc()).limit(limit).all()

    total_query = db.query(func.coalesce(func.sum(Expense.amount), 0))
    if category:
        total_query = total_query.filter(func.lower(Expense.category) == category.lower())
    if month:
        total_query = total_query.filter(extract("month", Expense.date) == month)
    if year:
        total_query = total_query.filter(extract("year", Expense.date) == year)

    total = total_query.scalar()
    return expenses, Decimal(str(total))