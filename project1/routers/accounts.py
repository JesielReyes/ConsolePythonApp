from typing import Literal

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from project1.database import SessionDep
from project1.service import account_service

router = APIRouter()

#used to tell pydantic that we can only recieve checking or savings as account type
AccountType = Literal["Checking", "Savings"]

#this class is used to define the structure and validation rules of the data our api will recieve when creating accounts
class AccountCreate(BaseModel):
    owner_id: int = Field(gt=0)
    account_type: AccountType
    balance: float = Field(default=0, ge=0)

#converts an account object to a dictionary so we can return it as a json
def account_to_dict(account):
    return {
        "account_number": account.account_number,
        "owner_id": account.owner_id,
        "balance": account.balance,
        "account_type": account.account_type
    }

#this can eitherbe used to get all acounts or just the accounts that have a specific owner id
@router.get("")
def list_accounts(
    session: SessionDep,
    owner_id: int | None = Query(default=None, gt=0)
):
    try:
        accounts = account_service.get_accounts(session, owner_id)

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

#gets a specific account using the account number
@router.get("/{account_number}")
def read_account(account_number: int, session: SessionDep):
    try:
        account = account_service.get_account(
            session,
            account_number
        )

        return account_to_dict(account)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

#this is used for account creation
@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_account(
    account_request: AccountCreate,
    session: SessionDep
):
    try:
        account = account_service.create_account(
            session=session,
            owner_id=account_request.owner_id,
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
def delete_account(account_number: int, session: SessionDep):
    try:
        account_service.delete_account(
            session,
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
