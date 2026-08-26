from models.transaction import AccountTransaction, TransferTransaction, Transaction, TransactionType, FetchTransactions
from sqlmodel import Session
from repository.accountsRepo import get_user_account_by_number, get_account_by_number
from repository.transactionRepo import save_transaction, get_transactions


def deposit(session: Session, acc: AccountTransaction):
    try:
        account = get_user_account_by_number(session, acc.user_id, acc.account_number)
        
        account.balance += acc.amount

        trans = Transaction(
            type=TransactionType.DEPOSIT,
            amount=acc.amount,
            from_user_id=acc.user_id,
            to_account_number=acc.account_number
        )

        save_transaction(trans)

        session.commit()
        session.refresh(account)

        return account
    
    except Exception:
        session.rollback()
        raise

def withdrawal(session: Session, acc: AccountTransaction):
    try:
        account = get_user_account_by_number(session, acc.user_id, acc.account_number)
        if not account:
            raise Exception("No Such Account")
        
        if account.balance < acc.amount:
            raise Exception("Insufficent Funds")
        
        account.balance -= acc.amount

        trans = Transaction(
            type=TransactionType.WITHDRAWL,
            amount=acc.amount,
            from_user_id=acc.user_id,
            from_account_number=acc.account_number
        )

        save_transaction(trans)

        session.commit()
        session.refresh(account)

        return account
    except Exception:
        session.rollback()
        raise


def transfer(session: Session, transfer: TransferTransaction):

    try:
        from_account = get_user_account_by_number(session, transfer.owner_id, transfer.from_account_number)
        if not from_account:
            raise Exception("Account Does Not Exist")
        
        to_account = get_account_by_number(session, transfer.to_account_number)
        if not to_account:
            raise Exception("Account Does Not Exist")
        
        if transfer.amount > from_account.balance:
            raise Exception("Insufficent Funds")
        
        from_account.balance -= transfer.amount
        to_account.balance += transfer.amount

        trans = Transaction(
            type=TransactionType.TRANSFER,
            amount=transfer.amount,
            from_user_id=transfer.owner_id,
            from_account_number=transfer.from_account_number,
            to_account_number=transfer.to_account_number
        )

        save_transaction(trans)

        session.commit()
        
    except Exception as e:
        session.rollback()
        raise


def fetchTransactions(session: Session, fetch: FetchTransactions):
    return get_transactions(session, fetch.user_id, fetch.account_number)