#import select so we can query our database
from sqlmodel import Session, select

from project1.models.account_model import AccountRecord

#used to create a new account in the database
def create_account(
    session: Session, #the session we will use to communicate with the db
    owner_id,
    account_type,
    balance
):
    #creates a new account record object
    account = AccountRecord(
        owner_id=owner_id,
        account_type=account_type,
        balance=balance
    )

    #adds and commits the account to the database, since account number is generated during insertion we must refresh so we can get the account number from the database
    session.add(account)
    session.commit()
    session.refresh(account)

    #returns the account to the api that called this function
    return account

#used to find an account using the account number
def get_account(session: Session, account_number):
    account = session.get(AccountRecord, account_number)

    if account is None:
        raise ValueError("Account not found")

    return account


def get_accounts(session: Session, owner_id=None):
    #select state is used to query our database
    statement = select(AccountRecord)

    #if no id is provided return all accounts, this will be for admins
    if owner_id is None:
        return session.exec(statement).all()

    #if an id is provided return only the accounts owned by that id
    statement = statement.where(AccountRecord.owner_id == owner_id)
    return session.exec(statement).all()


def delete_account(session: Session, account_number):
    account = get_account(session, account_number)

    #an account must have a zero balance to be deleted
    if account.get_balance() != 0:
        raise ValueError(
            "Account balance must be zero before deletion"
        )

    #deletes the account from our database
    session.delete(account)
    #commits the changes
    session.commit()

    return True