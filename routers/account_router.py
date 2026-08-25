from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from dummy_data import accounts


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


class TransactionRequest(BaseModel):
    amount: float


class TransferRequest(BaseModel):
    from_account_number: int
    to_account_number: int
    amount: float


def account_to_dict(account):
    return {
        "account_number": account.get_account_number(),
        "customer_id": account.get_customer_id(),
        "balance": account.get_balance(),
        "account_type": account.__class__.__name__
    }


@router.get("/")
def get_all_accounts():

    results = []

    for account in accounts.values():
        results.append(
            account_to_dict(account)
        )

    return results


@router.post("/transfer")
def transfer(request: TransferRequest):

    if request.from_account_number not in accounts:
        raise HTTPException(
            status_code=404,
            detail="Source account not found"
        )

    if request.to_account_number not in accounts:
        raise HTTPException(
            status_code=404,
            detail="Destination account not found"
        )

    from_account = accounts[
        request.from_account_number
    ]

    to_account = accounts[
        request.to_account_number
    ]

    success = from_account.withdraw(
        request.amount
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Transfer denied"
        )

    to_account.deposit(
        request.amount
    )

    return {
        "message": "Transfer successful",
        "from_balance": from_account.get_balance(),
        "to_balance": to_account.get_balance()
    }


@router.get("/{account_number}")
def get_account(account_number: int):

    if account_number not in accounts:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return account_to_dict(
        accounts[account_number]
    )


@router.post("/{account_number}/deposit")
def deposit(
    account_number: int,
    request: TransactionRequest
):

    if account_number not in accounts:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    account = accounts[account_number]

    if not account.deposit(request.amount):
        raise HTTPException(
            status_code=400,
            detail="Invalid deposit amount"
        )

    return {
        "message": "Deposit successful",
        "balance": account.get_balance()
    }


@router.post("/{account_number}/withdraw")
def withdraw(
    account_number: int,
    request: TransactionRequest
):

    if account_number not in accounts:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    account = accounts[account_number]

    if not account.withdraw(request.amount):
        raise HTTPException(
            status_code=400,
            detail="Withdrawal denied"
        )

    return {
        "message": "Withdrawal successful",
        "balance": account.get_balance()
    }