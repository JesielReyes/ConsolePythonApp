from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from repositories import account_repository
from repositories import user_repository


router = APIRouter()


TRANSACTION_HISTORY = []


class AccountTransaction(BaseModel):
    owner_id: int
    pin: int
    account_number: int
    amount: float = Field(gt=0)


class TransferTransaction(BaseModel):
    owner_id: int
    pin: int
    from_account_number: int
    to_account_number: int
    amount: float = Field(gt=0)


def _get_customer(owner_id):
    user = user_repository.get_user(owner_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.get_role() != "Customer":
        raise HTTPException(
            status_code=403,
            detail="Only customers can perform transactions"
        )

    return user


def _get_account(account_number):
    account = account_repository.get_account(account_number)

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return account


def _record_transaction(
    transaction_type,
    account,
    amount
):
    transaction = {
        "type": transaction_type,
        "owner_id": account.get_owner_id(),
        "account_number": account.get_account_number(),
        "amount": amount,
        "balance_after": account.get_balance()
    }

    TRANSACTION_HISTORY.append(transaction)

    return transaction


@router.post("/deposit")
def deposit(transaction: AccountTransaction):
    customer = _get_customer(transaction.owner_id)

    account = _get_account(
        transaction.account_number
    )

    if account.get_owner_id() != transaction.owner_id:
        raise HTTPException(
            status_code=403,
            detail="Account does not belong to this customer"
        )

    if not customer.check_pin(transaction.pin):
        raise HTTPException(
            status_code=403,
            detail="Invalid PIN"
        )

    if not account.deposit(transaction.amount):
        raise HTTPException(
            status_code=400,
            detail="Deposit failed"
        )

    return _record_transaction(
        "deposit",
        account,
        transaction.amount
    )


@router.post("/withdraw")
def withdraw(transaction: AccountTransaction):
    customer = _get_customer(transaction.owner_id)

    account = _get_account(
        transaction.account_number
    )

    if account.get_owner_id() != transaction.owner_id:
        raise HTTPException(
            status_code=403,
            detail="Account does not belong to this customer"
        )

    if not customer.check_pin(transaction.pin):
        raise HTTPException(
            status_code=403,
            detail="Invalid PIN"
        )

    if not account.withdraw(transaction.amount):
        raise HTTPException(
            status_code=400,
            detail="Withdrawal failed"
        )

    return _record_transaction(
        "withdrawal",
        account,
        transaction.amount
    )


@router.post("/transfer")
def transfer(transaction: TransferTransaction):
    customer = _get_customer(transaction.owner_id)

    if not customer.check_pin(transaction.pin):
        raise HTTPException(
            status_code=403,
            detail="Invalid PIN"
        )

    from_account = _get_account(
        transaction.from_account_number
    )

    to_account = _get_account(
        transaction.to_account_number
    )

    if from_account.get_owner_id() != transaction.owner_id:
        raise HTTPException(
            status_code=403,
            detail="Source account does not belong to this customer"
        )

    if not from_account.withdraw(transaction.amount):
        raise HTTPException(
            status_code=400,
            detail="Transfer failed"
        )

    to_account.deposit(transaction.amount)

    return {
        "withdrawal": _record_transaction(
            "transfer_out",
            from_account,
            transaction.amount
        ),

        "deposit": _record_transaction(
            "transfer_in",
            to_account,
            transaction.amount
        )
    }


@router.get("/{owner_id}/{account_number}")
def read_transaction_history(
    owner_id: int,
    account_number: int
):
    account = _get_account(account_number)

    if account.get_owner_id() != owner_id:
        raise HTTPException(
            status_code=403,
            detail="Account does not belong to this customer"
        )

    history = [
        transaction
        for transaction in TRANSACTION_HISTORY
        if transaction["owner_id"] == owner_id
        and transaction["account_number"] == account_number
    ]

    return {
        "owner_id": owner_id,
        "account_number": account_number,
        "transactions": history
    }