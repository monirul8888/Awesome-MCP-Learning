from fastmcp import FastMCP
from app.database import SessionLocal, engine, Base
from app import crud
from app.schemas import ExpenseCreate
from datetime import date

Base.metadata.create_all(bind=engine)

mcp = FastMCP("Student Expense Tracker")


def get_db():
    return SessionLocal()







@mcp.tool
def add_expense(amount: float, category: str, description: str = "") -> str:
    """Add a new expense. Categories: Food, Transport, Books, Rent, Internet, Entertainment, Medical, Stationary"""
    if amount <= 0:
        return "❌ Amount must be greater than 0."

    db = get_db()
    try:
        data = ExpenseCreate(
            amount=amount,
            category=category,
            description=description or None,
            date=None  # ← always None, DB default হবে today
        )
        expense = crud.create_expense(db, data)
        return (
            f"✅ Expense saved!\n"
            f"ID: #{expense.id}\n"
            f"Amount: ৳{float(expense.amount):.2f}\n"
            f"Category: {expense.category}\n"
            f"Note: {expense.description or '—'}\n"
            f"Date: {expense.date}"
        )
    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        db.close()



@mcp.tool
def show_expenses(category: str = "", month: int = 0, year: int = 0, limit: int = 20) -> str:
    """Show expenses with filters."""
    db = get_db()
    try:
        expenses, total = crud.get_expenses(
            db,
            category=category or None,
            month=month or None,
            year=year or None,
            limit=limit,
        )

        if not expenses:
            return "📭 No expenses found."

        lines = ["📊 Expense Report", "-" * 40]

        for e in expenses:
            lines.append(
                f"#{e.id} | {e.date} | {e.category} | ৳{e.amount:.2f} | {e.description or '—'}"
            )

        lines.append("-" * 40)
        lines.append(f"Total: ৳{total:.2f}")
        lines.append(f"Records: {len(expenses)}")

        return "\n".join(lines)
    finally:
        db.close()