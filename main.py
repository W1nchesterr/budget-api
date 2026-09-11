from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime

from database import Base, engine, get_db
from models import Transaction
from schemas import TransactionCreate, TransactionResponse, BudgetSummary

app = FastAPI(title="Şəxsi Büdcə və Xərc İdarəetmə Sistemi")

Base.metadata.create_all(bind=engine)


@app.get("/transactions/", response_model=list[TransactionResponse])
def get_transactions(
    type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    
    try:
        query = db.query(Transaction)

        if type:
            if type not in ("income", "expense"):
                raise HTTPException(status_code=400, detail="type yalnız 'income' və ya 'expense' ola bilər")
            query = query.filter(Transaction.type == type)

        if start_date:
            query = query.filter(Transaction.created_at >= start_date)

        if end_date:
            query = query.filter(Transaction.created_at <= end_date)

        return query.all()
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Sorğu icra edilə bilmədi: {str(e)}")


@app.get("/budget/summary", response_model=BudgetSummary)
def get_budget_summary(db: Session = Depends(get_db)):
    
    try:
        transactions = db.query(Transaction).all()

        total_income = sum(t.amount for t in transactions if t.type == "income")
        total_expense = sum(t.amount for t in transactions if t.type == "expense")

        balance = total_income - total_expense

        return BudgetSummary(
            total_income=total_income,
            total_expense=total_expense,
            balance=balance,
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hesabat hazırlana bilmədi: {str(e)}")


@app.post("/transactions/", response_model=TransactionResponse, status_code=201)
def create_transaction(tx: TransactionCreate, db: Session = Depends(get_db)):
    
    try:
        new_tx = Transaction(
            amount=tx.amount,
            type=tx.type,
            category=tx.category,
        )

        db.add(new_tx)
        db.commit()
        db.refresh(new_tx)

        return new_tx
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Əməliyyat əlavə edilə bilmədi: {str(e)}")