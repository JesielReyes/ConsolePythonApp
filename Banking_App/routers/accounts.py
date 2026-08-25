from fastapi import APIRouter

router = APIRouter()

ACCOUNTS = [
    {"id": 1, "user_id": 1, "account_number": "123456789", "balance": 1000, "account_type": "checking"},
    {"id": 2, "user_id": 2, "account_number": "987654321", "balance": 500, "account_type": "savings"},
    ]

@router.get("/{account_id}")
def read_account(account_id: int):
    account = {}
    for acc in ACCOUNTS:
        if acc["id"] == account_id:
            account = acc
            break
    return {"account_id": account_id, "account": account}

@router.get("/withdraw/{account_id}/{amount}")
def withdraw(account_id: int, amount: float):
    for acc in ACCOUNTS:
        if acc["id"] == account_id:
            if acc["balance"] >= amount:
                acc["balance"] -= amount
                return {"account_id": account_id, "new_balance": acc["balance"]}
            else:
                return {"error": "Insufficient funds"}
    return {"error": "Account not found"}

@router.get("/deposit/{account_id}/{amount}")
def deposit(account_id: int, amount: float):
    for acc in ACCOUNTS:
        if acc["id"] == account_id:
            acc["balance"] += amount
            return {"account_id": account_id, "new_balance": acc["balance"]}
    return {"error": "Account not found"}