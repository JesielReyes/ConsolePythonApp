from fastapi import FastAPI
from routers import accounts, users

app = FastAPI()

app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(users.router, prefix="/users", tags=["users"])

USERS = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]
ACCOUNTS = [
    {"id": 1, "user_id": 1, "account_number": "123456789", "balance": 1000, "account_type": "checking"},
    {"id": 2, "user_id": 2, "account_number": "987654321", "balance": 500, "account_type": "savings"},
    ]

