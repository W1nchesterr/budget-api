from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Mənfi və ya 0 ola bilməz")
    type: Literal["income", "expense"]
    category: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  


class BudgetSummary(BaseModel):
    total_income: float
    total_expense: float
    balance: float