from typing import Literal

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from data import ACCOUNTS

router = APIRouter()

AccountType = Literal["checking", "savings"]


class AccountCreate(BaseModel):
    owner_id: int = Field(gt=0)
    account_type: AccountType
    balance: float = Field(default=0, ge=0)


class AccountUpdate(BaseModel):
    account_type: AccountType | None = None


def _find_account(account_id: int):
    for account in ACCOUNTS:
        if account["id"] == account_id:
            return account
    raise HTTPException(status_code=404, detail="Account not found")


def _next_account_number():
    account_numbers = [int(account["account_number"]) for account in ACCOUNTS]
    next_account_number = max(account_numbers, default=10000000) + 1
    return str(next_account_number)


@router.get("")
def list_accounts(owner_id: int | None = Query(default=None, gt=0)):
    if owner_id is None:
        return {"accounts": ACCOUNTS}
    return {"accounts": [account for account in ACCOUNTS if account["owner_id"] == owner_id]}


@router.get("/{account_id}")
def read_account(account_id: int):
    return _find_account(account_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_account(account_request: AccountCreate):
    account = {
        "id": max((account["id"] for account in ACCOUNTS), default=0) + 1,
        "owner_id": account_request.owner_id,
        "account_number": _next_account_number(),
        "balance": account_request.balance,
        "account_type": account_request.account_type,
    }
    ACCOUNTS.append(account)
    return account

#admin specific
@router.delete("/{account_id}")
def delete_account(account_id: int):
    account = _find_account(account_id)
    if account["balance"] != 0:
        raise HTTPException(status_code=400, detail="Account balance must be zero before deletion")
    ACCOUNTS.remove(account)
    return {"account_id": account_id, "deleted": True}