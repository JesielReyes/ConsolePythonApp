from fastapi import APIRouter, HTTPException
from models.transaction import AccountTransaction, TransferTransaction, FetchTransactions
from database import SessionDep
import service.transaction_service
from dto import ResponseDTO


# router = APIRouter()


@router.post("/deposit")
def deposit(transaction: AccountTransaction, session: SessionDep):
    
    try:
        account = service.transaction_service.deposit(session, transaction)
        return ResponseDTO(200, "Deposit Success", account)
    except Exception as e:
        return ResponseDTO(500, "Error", str(e))

@router.post("/withdraw")
def withdraw(transaction: AccountTransaction, session: SessionDep):
    
    try:
        account = service.transaction_service.withdrawal(session, transaction)
        return ResponseDTO(200, "Deposit Success", account)
    except Exception as e:
        return ResponseDTO(500, "Error", str(e))

@router.post("/transfer")
def transfer(transaction: TransferTransaction, session: SessionDep):
    
    try:
        service.transaction_service.transfer(session, transaction)
        return ResponseDTO(200, "Transfer Success", None)
    except Exception as e:
        return ResponseDTO(500, "Error", str(e))


@router.get("/{owner_id}/{account_number}")
def read_transaction_history(
    fetchTransaction: FetchTransactions, 
    session: SessionDep
):
    try:
        all = service.transaction_service.fetchTransactions(session, fetchTransaction)
        return ResponseDTO(
            200,
            "Fetch Success",
            all
        )
    except Exception as e:
        return ResponseDTO(
            500,
            "Error",
            str(e)
        )
