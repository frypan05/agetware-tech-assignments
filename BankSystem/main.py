
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from database import SessionLocal
from models import Loan, Transaction

app = FastAPI()


class LoanRequest(BaseModel):
    customer_id: int
    principal: float
    period_years: int
    interest_rate: float

class PaymentRequest(BaseModel):
    loan_id: int
    amount_paid: float


@app.post("/lend")
def lend_loan(request: LoanRequest):
    session = SessionLocal()
    
    interest = (request.principal * request.period_years * request.interest_rate) / 100
    total_amount = request.principal + interest
    emi = total_amount / (request.period_years * 12)
    
    loan = Loan(
        customer_id=request.customer_id,
        principal=request.principal,
        interest_rate=request.interest_rate,
        period_years=request.period_years,
        total_amount=total_amount,
        emi=emi,
        balance=total_amount,
        emi_left=request.period_years * 12
    )
    
    session.add(loan)
    session.commit()
    
    return {"loan_id": loan.loan_id, "emi": emi, "total_amount": total_amount}


@app.post("/payment")
def make_payment(request: PaymentRequest):
    session = SessionLocal()
    loan = session.query(Loan).filter(Loan.loan_id == request.loan_id).first()
    
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    loan.balance -= request.amount_paid
    emi_deducted = request.amount_paid / loan.emi
    loan.emi_left = max(0, loan.emi_left - int(emi_deducted))
    
    transaction = Transaction(loan_id=loan.loan_id, amount_paid=request.amount_paid, date=datetime.now())
    session.add(transaction)
    session.commit()
    
    return {"balance": loan.balance, "emi_left": loan.emi_left}

@app.get("/ledger/{loan_id}")
def get_ledger(loan_id: int):
    session = SessionLocal()
    loan = session.query(Loan).filter(Loan.loan_id == loan_id).first()
    
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    transactions = session.query(Transaction).filter(Transaction.loan_id == loan_id).all()
    
    return {
        "loan_id": loan.loan_id,
        "emi": loan.emi,
        "balance": loan.balance,
        "emi_left": loan.emi_left,
        "transactions": [{"amount_paid": t.amount_paid, "date": t.date} for t in transactions]
    }

@app.get("/account/{customer_id}")
def account_overview(customer_id: int):
    session = SessionLocal()
    loans = session.query(Loan).filter(Loan.customer_id == customer_id).all()
    
    if not loans:
        raise HTTPException(status_code=404, detail="No loans found")
    
    return [
        {
            "loan_id": loan.loan_id,
            "principal": loan.principal,
            "total_amount": loan.total_amount,
            "emi": loan.emi,
            "interest_rate": loan.interest_rate,
            "amount_paid": loan.total_amount - loan.balance,
            "balance": loan.balance,
            "emi_left": loan.emi_left
        }
        for loan in loans
    ]
