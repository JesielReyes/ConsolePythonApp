from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from data import ACCOUNTS, TRANSACTION_HISTORY

router = APIRouter()


class AccountTransaction(BaseModel):
	owner_id: int
	account_number: str
	amount: float = Field(gt=0)


class TransferTransaction(BaseModel):
	owner_id: int
	account_number: str
	destination_owner_id: int
	destination_account_number: str
	amount: float = Field(gt=0)


def _find_account(owner_id: int, account_number: str):
	for account in ACCOUNTS:
		if account["owner_id"] == owner_id and account["account_number"] == account_number:
			return account
	raise HTTPException(status_code=404, detail="Account not found for this owner")


def _record_transaction(transaction_type: str, account, amount: float):
	transaction = {
		"type": transaction_type,
		"owner_id": account["owner_id"],
		"account_number": account["account_number"],
		"amount": amount,
		"balance_after": account["balance"],
	}
	TRANSACTION_HISTORY.append(transaction)
	return transaction


@router.post("/deposit")
def deposit(transaction: AccountTransaction):
	account = _find_account(transaction.owner_id, transaction.account_number)
	account["balance"] += transaction.amount
	return _record_transaction("deposit", account, transaction.amount)


@router.post("/withdraw")
def withdraw(transaction: AccountTransaction):
	account = _find_account(transaction.owner_id, transaction.account_number)
	if transaction.amount > account["balance"]:
		raise HTTPException(status_code=400, detail="Insufficient funds")
	account["balance"] -= transaction.amount
	return _record_transaction("withdrawal", account, transaction.amount)


@router.post("/transfer")
def transfer(transaction: TransferTransaction):
	source = _find_account(transaction.owner_id, transaction.account_number)
	destination = _find_account(
		transaction.destination_owner_id,
		transaction.destination_account_number,
	)
	if transaction.amount > source["balance"]:
		raise HTTPException(status_code=400, detail="Insufficient funds")
	source["balance"] -= transaction.amount
	destination["balance"] += transaction.amount
	return {
		"withdrawal": _record_transaction("transfer_out", source, transaction.amount),
		"deposit": _record_transaction("transfer_in", destination, transaction.amount),
	}


@router.get("/{owner_id}/{account_number}")
def read_transaction_history(owner_id: int, account_number: str):
	_find_account(owner_id, account_number)
	history = [
		transaction
		for transaction in TRANSACTION_HISTORY
		if transaction["owner_id"] == owner_id
		and transaction["account_number"] == account_number
	]
	return {
		"owner_id": owner_id,
		"account_number": account_number,
		"transactions": history,
	}
