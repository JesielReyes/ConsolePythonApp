from sqlmodel import Field, SQLModel
from enum import Enum
from pydantic import BaseModel

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWL = "withdrawl"
    PURCHASE = "purchase" 
    TRANSFER = "transfer"

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type: TransactionType
    amount: int
    category: str | None = Field(default=None)
    from_user_id: int
    from_account_number: int | None = Field(default=None)
    to_account_number: int | None = Field(default=None)

class AccountTransaction(BaseModel):
    user_id: int
    account_number: int
    amount: float = Field(gt=0)


class TransferTransaction(BaseModel):
    owner_id: int
    from_account_number: int
    to_account_number: int
    amount: float = Field(gt=0)

class FetchTransactions(BaseModel):
    user_id: int
    account_number: int
