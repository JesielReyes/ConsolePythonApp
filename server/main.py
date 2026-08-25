from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, Field


class Category(str, Enum):
    groceries = "groceries"
    dining = "dining"
    transport = "transport"
    entertainment = "entertainment"
    bills = "bills"
    other = "other"


class PurchaseCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    merchant: str = Field(min_length=1, max_length=100)
    category: Category | None = None


class LedgerEntry(BaseModel):
    id: UUID
    purchase_id: UUID
    entry_type: str
    amount: Decimal


class PurchaseResponse(BaseModel):
    id: UUID
    account_id: str
    amount: Decimal
    merchant: str
    category: Category | None
    ledger_entry: LedgerEntry


class Account:
    def __init__(self) -> None:
        self.balance = Decimal("0.00")


app = FastAPI(title="ConsolePythonApp POC API", version="0.1.0")
ACCOUNTS: dict[str, Account] = {}


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/accounts/{account_id}/purchases",
    response_model=PurchaseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["purchases"],
)
def post_purchase(account_id: str, purchase: PurchaseCreate) -> PurchaseResponse:
    account = ACCOUNTS.setdefault(account_id, Account())
    purchase_id = uuid4()
    account.balance -= purchase.amount

    ledger_entry = LedgerEntry(
        id=uuid4(),
        purchase_id=purchase_id,
        entry_type="purchase_debit",
        amount=-purchase.amount,
    )
    return PurchaseResponse(
        id=purchase_id,
        account_id=account_id,
        ledger_entry=ledger_entry,
        **purchase.model_dump(),
    )