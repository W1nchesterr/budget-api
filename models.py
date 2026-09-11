from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Transaction(Base):  
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)          
    category = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())