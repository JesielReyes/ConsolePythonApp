from fastapi import APIRouter, HTTPException
from uuid import UUID

from database import SessionDep
from models.transaction import DepositTransaction, TransactionType, TransferTransaction, WithdrawalTransaction
from service import transaction_service
from service.user_service import get_db_user

router = APIRouter()


@router.post("/deposit")
def deposit(transaction: DepositTransaction, session: SessionDep, owner_id: UUID):
    try:
        if get_db_user(session, owner_id).is_admin:
            raise HTTPException(status_code=403, detail="Admins cannot make transactions")
        return transaction_service.deposit(session, transaction, owner_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/withdraw")
def withdraw(transaction: WithdrawalTransaction, session: SessionDep, owner_id: UUID):
    try:
        if get_db_user(session, owner_id).is_admin:
            raise HTTPException(status_code=403, detail="Admins cannot make transactions")
        return transaction_service.withdrawal(session, transaction, owner_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/purchase")
def purchase(transaction: WithdrawalTransaction, session: SessionDep, owner_id: UUID):
    try:
        if get_db_user(session, owner_id).is_admin:
            raise HTTPException(status_code=403, detail="Admins cannot make transactions")
        return transaction_service.withdrawal(session, transaction, owner_id, TransactionType.PURCHASE)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/transfer")
def transfer(transaction: TransferTransaction, session: SessionDep, owner_id: UUID):
    try:
        if get_db_user(session, owner_id).is_admin:
            raise HTTPException(status_code=403, detail="Admins cannot make transactions")
        transaction_service.transfer(session, transaction, owner_id)
        return {"message": "Transfer success"}
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=400, detail="Transfer could not be completed") from error

 
@router.get("")
def read_transaction_history(session: SessionDep, owner_id: UUID):
    user = get_db_user(session, owner_id)
    return transaction_service.fetch_transactions(session, owner_id, user.is_admin)


@router.get("/owners/{owner_id}/categories")
def read_transaction_categories(
    owner_id: int,
    session: SessionDep
):
    try:
        categories = service.transaction_service.fetchTransactionCategories(session, owner_id)
        return ResponseDTO(
            200,
            "Fetch Success",
            categories
        )
    except Exception as e:
        return ResponseDTO(
            500,
            "Error",
            str(e)
        )
   