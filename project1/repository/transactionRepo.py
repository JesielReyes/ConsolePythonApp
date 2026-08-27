from models.transaction import Transaction
from sqlmodel import Session, select
from sqlalchemy import or_
from uuid import UUID

def save_transaction(session: Session, transaction: Transaction):
    session.add(transaction)
    return transaction

def get_transactions(session: Session, owner_id: UUID, is_admin=False):
    statement = select(Transaction)
    if not is_admin:
        statement = statement.where(
            or_(Transaction.from_owner_id == owner_id, Transaction.to_owner_id == owner_id)
        )
    return session.exec(statement).all()