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

    