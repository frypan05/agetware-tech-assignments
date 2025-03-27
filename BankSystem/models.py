# models.py (Database Models)
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from database import Base

class Loan(Base):
    __tablename__ = "loans"
    
    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    principal = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    period_years = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    emi = Column(Float, nullable=False)
    balance = Column(Float, nullable=False)
    emi_left = Column(Integer, nullable=False)

class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(Integer, ForeignKey("loans.loan_id"), nullable=False)
    amount_paid = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)