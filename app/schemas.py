from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class ExpenseCreate(BaseModel):
    amount      : Decimal        = Field(..., gt=0)
    category    : str            = Field(..., min_length=1, max_length=100)
    description : Optional[str]  = None
    date        : Optional[date] = None   # ← model_config সরানো হয়েছে


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