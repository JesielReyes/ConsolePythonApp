from pydantic import BaseModel


class CreateAccountRequest(BaseModel):
    customer_id: int
    account_type: str
    balance: float = 0


class TransactionRequest(BaseModel):
    amount: float