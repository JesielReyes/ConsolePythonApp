from project1.models.transaction import Transaction
from sqlmodel import Session, select
from sqlalchemy import or_

def save_transaction(session: Session, transaction: Transaction):
    session.add(transaction)
    return transaction

def get_transactions(session: Session, user_id: int, account_number: int):
    statement = select(Transaction).where(
        Transaction.from_user_id == user_id,
        or_(
            Transaction.from_account_number == account_number,
            Transaction.to_account_number == account_number
        )
    )
    return session.exec(statement).all()