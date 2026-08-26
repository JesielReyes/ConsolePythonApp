from models.transaction import FetchTransactions, defaultCategories

from sqlmodel import Session

from models.transaction import DepositTransaction, Transaction, TransactionType, TransferTransaction, WithdrawalTransaction
from repository.accountsRepo import get_account_by_number, get_user_account_by_number
from repository.transactionRepo import get_transactions, save_transaction


def deposit(session: Session, request: DepositTransaction, owner_id):
    account = get_user_account_by_number(session, owner_id, request.account_number)
    if account is None:
        raise ValueError("Account does not exist")
    account.balance += float(request.amount)
    save_transaction(session, Transaction(
        type=TransactionType.DEPOSIT, from_owner_id=owner_id,
        from_owner_account_number=request.account_number,
        description=None, category=None, amount=request.amount,
    ))
    session.commit()
    session.refresh(account)
    return account


def withdrawal(session: Session, request: WithdrawalTransaction, owner_id, transaction_type=TransactionType.WITHDRAWAL):
    account = get_user_account_by_number(session, owner_id, request.account_number)
    if account is None:
        raise ValueError("Account does not exist")
    amount = float(request.amount)
    current = account.balance
    if account.account_type != "Checking" and amount > current:
        raise ValueError("Insufficient funds")
    if account.account_type == "Checking" and current - amount < -50000:
        raise ValueError("Overdraft limit exceeded")
    account.balance = current - amount
    save_transaction(session, Transaction(
        type=transaction_type, from_owner_id=owner_id,
        from_owner_account_number=request.account_number,
        description=request.description, category=request.category, amount=request.amount,
    ))
    session.commit()
    session.refresh(account)
    return account


def transfer(session: Session, request: TransferTransaction, owner_id):
    try:
        source = get_user_account_by_number(session, owner_id, request.from_account_number)
        target = get_account_by_number(session, request.to_account_number)
        if source is None or target is None or target.owner_id != str(request.to_owner_id):
            raise ValueError("Account does not exist or is not owned by the specified user")
        amount = float(request.amount)
        if amount > source.balance:
            raise ValueError("Insufficient funds")
        source.balance -= amount
        target.balance += amount
        save_transaction(session, Transaction(
            type=TransactionType.TRANSFER, from_owner_id=owner_id,
            from_owner_account_number=request.from_account_number,
            to_owner_id=request.to_owner_id, to_owner_account_number=request.to_account_number,
            description=None, category=None, amount=request.amount,
        ))
        session.commit()
    except Exception:
        session.rollback()
        raise


def fetch_transactions(session: Session, owner_id, is_admin=False):
    return get_transactions(session, owner_id, is_admin)

def fetchTransactionCategories(session: Session, owner_id):
    # TODO: support custom categories in the future
    return list(defaultCategories)

