from fastapi import APIRouter

router = APIRouter()

USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]
ACCOUNTS = [
    {"id": 1, "user_id": 1, "account_number": "123456789", "balance": 1000, "account_type": "checking"},
    {"id": 2, "user_id": 2, "account_number": "987654321", "balance": 500, "account_type": "savings"},
    ]


@router.get("/{user_id}")
def read_user(user_id: int):
    name = ""
    for user in USERS:
        if user["id"] == user_id:
            name = user["name"]
            break
    acc = []
    for account in ACCOUNTS:
        if account["user_id"] == user_id:
            acc.append(account)
    return {"user_id": user_id, "name": name, "accounts": acc}