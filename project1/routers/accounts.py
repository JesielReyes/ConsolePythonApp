from typing import Literal

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlmodel import select
from database import SessionDep
from service import account_service


router = APIRouter()

AccountType = Literal["Checking", "Savings"]


class AccountCreate(BaseModel):
    owner_id: int = Field(gt=0)
    pin: int = Field(gt=0)
    account_type: AccountType
    balance: float = Field(default=0, ge=0)


def account_to_dict(account):
    return {
        "account_number": account.get_account_number(),
        "owner_id": account.get_owner_id(),
        "balance": account.get_balance(),
        "account_type": account.get_account_type()
    }


@router.get("")
def list_accounts(
    owner_id: int | None = Query(default=None, gt=0)
):
    try:
        accounts = account_service.get_accounts(owner_id)

        return {
            "accounts": [
                account_to_dict(account)
                for account in accounts
            ]
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get("/{account_number}")
def read_account(account_number: int):
    try:
        account = account_service.get_account(
            account_number
        )

        return account_to_dict(account)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_account(
    account_request: AccountCreate
):
    try:
        account = account_service.create_account(
            owner_id=account_request.owner_id,
            pin=account_request.pin,
            account_type=account_request.account_type,
            balance=account_request.balance
        )

        return account_to_dict(account)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.delete("/{account_number}")
def delete_account(account_number: int):
    try:
        account_service.delete_account(
            account_number
        )

        return {
            "account_number": account_number,
            "deleted": True
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
