# 🎓 Student Expense Tracker — MCP Server with FastAPI + PostgreSQL

A personal expense tracker that works inside **Claude Desktop** as an MCP tool, backed by a **FastAPI** REST API and **PostgreSQL** database.

---

## 📁 Project Structure

```
Expense/
│
├── app/
│   ├── __init__.py
│   ├── database.py        # SQLAlchemy engine + session
│   ├── models.py          # DB table models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # DB operations
│   └── api/
│       ├── __init__.py
│       └── routes.py      # FastAPI routes
│
├── tools/
│   ├── __init__.py
│   └── server.py          # FastMCP tools (add/show expense)
│
├── .env                   # DB credentials (never commit this)
├── main.py                # FastAPI entry point
├── mcp_server.py          # MCP entry point
└── pyproject.toml         # uv project config
```

---

## ✅ Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.10+ | [python.org](https://python.org) |
| uv | latest | `pip install uv` |
| PostgreSQL | 14+ | [postgresql.org](https://www.postgresql.org/download/) |
| Claude Desktop | latest | [claude.ai/download](https://claude.ai/download) |
| Postman (optional) | any | [postman.com](https://postman.com) |

> ⚠️ Open Claude Desktop at least once after installing so it creates its config folder.

---

## 🚀 Setup Guide

### Step 1 — Clone / Create Project

```powershell
mkdir D:\Python\MCP\Expense
cd D:\Python\MCP\Expense
uv init
uv add fastmcp fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

### Step 2 — Create Folder Structure

```powershell
mkdir app
mkdir app\api
mkdir tools
New-Item app\__init__.py -Force
New-Item app\api\__init__.py -Force
New-Item tools\__init__.py -Force
```

### Step 3 — Create `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=expense_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### Step 4 — Create PostgreSQL Database

Open **pgAdmin** or **psql** and run:

```sql
CREATE DATABASE expense_db;
```

> The `expenses` table is created automatically when the server starts.

---

## 📄 Source Files

### `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### `app/models.py`

```python
from sqlalchemy import Column, Integer, Numeric, String, Text, Date, DateTime, func
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id          = Column(Integer, primary_key=True, index=True)
    amount      = Column(Numeric(10, 2), nullable=False)
    category    = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    date        = Column(Date, nullable=False, server_default=func.current_date())
    created_at  = Column(DateTime, server_default=func.now())
```

### `app/schemas.py`

```python
from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

class ExpenseCreate(BaseModel):
    amount      : Decimal        = Field(..., gt=0)
    category    : str            = Field(..., min_length=1, max_length=100)
    description : Optional[str]  = None
    date        : Optional[date] = None   # None = today by default

class ExpenseResponse(BaseModel):
    id          : int
    amount      : Decimal
    category    : str
    description : Optional[str]
    date        : date
    created_at  : datetime

    model_config = {"from_attributes": True}

class ExpenseSummary(BaseModel):
    total    : Decimal
    count    : int
    expenses : list[ExpenseResponse]
```

### `app/crud.py`

```python
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
```

### `app/api/routes.py`

```python
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
    return ExpenseSummary(total=total, count=len(expenses), expenses=expenses)
```

### `main.py`

```python
from fastapi import FastAPI
from app.database import engine, Base
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title       = "Student Expense Tracker API",
    description = "Track your daily expenses as a student",
    version     = "1.0.0",
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Student Expense Tracker is running 🎓"}
```

### `tools/server.py`

```python
from fastmcp import FastMCP
from app.database import SessionLocal, engine, Base
from app import crud
from app.schemas import ExpenseCreate

Base.metadata.create_all(bind=engine)

mcp = FastMCP("Student Expense Tracker")

def get_db():
    return SessionLocal()

@mcp.tool
def add_expense(amount: float, category: str, description: str = "") -> str:
    """
    Add a new expense.
    Categories: Food, Transport, Books, Rent, Internet, Entertainment, Medical, Stationary
    """
    if amount <= 0:
        return "❌ Amount must be greater than 0."

    db = get_db()
    try:
        data = ExpenseCreate(
            amount=amount,
            category=category,
            description=description or None,
            date=None   # DB default = today
        )
        expense = crud.create_expense(db, data)
        return (
            f"✅ Expense saved!\n"
            f"ID       : #{expense.id}\n"
            f"Amount   : ৳{float(expense.amount):.2f}\n"
            f"Category : {expense.category}\n"
            f"Note     : {expense.description or '—'}\n"
            f"Date     : {expense.date}"
        )
    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        db.close()

@mcp.tool
def show_expenses(category: str = "", month: int = 0, year: int = 0, limit: int = 20) -> str:
    """
    Show expense history.
    category: Food / Transport / Books etc. (empty = all)
    month: 1-12 (0 = all)
    year: e.g. 2026 (0 = all)
    """
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

        lines = ["📊 Expense Report", "─" * 50]
        for e in expenses:
            lines.append(
                f"#{e.id:>3} | {e.date} | {e.category:<14} | "
                f"৳{float(e.amount):>8.2f} | {e.description or '—'}"
            )
        lines.append("─" * 50)
        lines.append(f"Total  : ৳{float(total):.2f}")
        lines.append(f"Records: {len(expenses)}")
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        db.close()
```

### `mcp_server.py`

```python
from tools.server import mcp

if __name__ == "__main__":
    mcp.run()
```

---

## ▶️ Running the Project

### Run FastAPI Server

```powershell
uv run python -m uvicorn main:app --reload
```

Visit → `http://localhost:8000/docs` for Swagger UI

### Test MCP Server Locally

```powershell
uv run python mcp_server.py
```

You should see the FastMCP banner. Press `Ctrl+C` to stop.

---

## 🔌 Connect to Claude Desktop

### Find your config file path

**Standard install:**
```
C:\Users\<username>\AppData\Roaming\Claude\claude_desktop_config.json
```

**Microsoft Store install:**
```
C:\Users\<username>\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json
```

> To find which one applies, run:
> ```powershell
> Get-ChildItem "$env:LOCALAPPDATA" -Filter "*Claude*" -Recurse -ErrorAction SilentlyContinue
> ```

### Write the config (replace path as needed)

```powershell
# Find uv path first
where.exe uv

# Write config (Standard install)
$config = '{"mcpServers":{"expense":{"command":"C:\\Users\\<username>\\.local\\bin\\uv.exe","args":["--directory","D:\\Python\\MCP\\Expense","run","python","mcp_server.py"]}}}'

[System.IO.File]::WriteAllText("$env:APPDATA\Claude\claude_desktop_config.json", $config)
```

> ⚠️ Always use `[System.IO.File]::WriteAllText()` — PowerShell's `Out-File` adds a BOM that breaks JSON.

### Restart Claude Desktop

1. System tray → right-click Claude → **Quit**
2. Reopen Claude Desktop
3. Go to **Settings (⚙) → Developer** — `expense` server should appear ✅

---

## 💬 How to Use in Claude Desktop

Just type naturally:

```
Add expense 150 taka for Food, lunch at cafeteria
Add expense 50 for Transport, rickshaw to university
Add expense 500 for Books, data structures book

Show all my expenses
Show expenses for Food
Show expenses for month 6 year 2026
```

---

## 🌐 API Endpoints (Postman / Swagger)

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `http://localhost:8000/` | Health check |
| `POST` | `http://localhost:8000/expenses/` | Add expense |
| `GET` | `http://localhost:8000/expenses/` | All expenses |
| `GET` | `http://localhost:8000/expenses/?category=Food` | Filter by category |
| `GET` | `http://localhost:8000/expenses/?month=6&year=2026` | Filter by month/year |

**POST Body example:**
```json
{
  "amount": 150.00,
  "category": "Food",
  "description": "Lunch at cafeteria"
}
```

---

## 🏷️ Expense Categories

| Category | Examples |
|----------|----------|
| Food | Lunch, dinner, snacks |
| Transport | Rickshaw, bus, CNG |
| Books | Textbooks, printouts |
| Rent | Mess/hostel payment |
| Internet | Mobile data, WiFi |
| Entertainment | Netflix, games |
| Stationary | Pen, paper, copies |
| Medical | Medicine, doctor visit |

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `uv trampoline failed` | uv script path broken | Use `uv run python mcp_server.py` instead |
| `No module named fastmcp.__main__` | fastmcp can't run as module | Use manual config method |
| MCP server not showing in Claude | Wrong config file path | Check if Store vs standard install |
| `Expecting value: line 1 column 1` | Config file has BOM encoding | Use `WriteAllText()` not `Out-File` |
| Date field rejected | `model_config` in wrong schema | Remove from `ExpenseCreate`, keep in `ExpenseResponse` only |
| `mcp` folder import conflict | Folder named `mcp` conflicts with mcp package | Rename folder to `tools` |

---

## 📋 Quick Commands Reference

```powershell
# Run FastAPI
uv run python -m uvicorn main:app --reload

# Test MCP server
uv run python mcp_server.py

# Find uv path
where.exe uv

# Check config
cat "$env:APPDATA\Claude\claude_desktop_config.json"

# Find Claude install type
Get-ChildItem "$env:LOCALAPPDATA" -Filter "*Claude*" -Recurse -ErrorAction SilentlyContinue
```
