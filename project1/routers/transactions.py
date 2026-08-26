from fastapi import APIRouter, HTTPException
from project1.models.transaction import AccountTransaction, TransferTransaction, FetchTransactions
from project1.database import SessionDep
import project1.service.transaction_service
from project1.dto import ResponseDTO


router = APIRouter()


@router.post("/deposit")
def deposit(transaction: AccountTransaction, session: SessionDep):
    
    try:
        account = project1.service.transaction_service.deposit(session, transaction)
        return ResponseDTO(200, "Deposit Success", account)
    except Exception as e:
        return ResponseDTO(500, "Error", str(e))

@router.post("/withdraw")
def withdraw(transaction: AccountTransaction, session: SessionDep):
    
    try:
        account = project1.service.transaction_service.withdrawal(session, transaction)
        return ResponseDTO(200, "Deposit Success", account)
    except Exception as e:
        return ResponseDTO(500, "Error", str(e))

@router.post("/transfer")
def transfer(transaction: TransferTransaction, session: SessionDep):
    
    try:
        project1.service.transaction_service.transfer(session, transaction)
        return ResponseDTO(200, "Transfer Success", None)
    except Exception as e:
        return ResponseDTO(500, "Error", str(e))


@router.get("/{owner_id}/{account_number}")
def read_transaction_history(
    fetchTransaction: FetchTransactions, 
    session: SessionDep
):
    try:
        all = project1.service.transaction_service.fetchTransactions(session, fetchTransaction)
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
