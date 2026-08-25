from fastapi import FastAPI
from project1.routers import transactions
from routers import accounts, users

app = FastAPI()

app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])