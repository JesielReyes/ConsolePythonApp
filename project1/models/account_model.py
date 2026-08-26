#sqlmodel is base class used to define database
#field is used to configure individual columns of the table
from sqlmodel import Field, SQLModel

#this cass is used to represent the overall databse table structure, shows us what each row will contain
class AccountRecord(SQLModel, table=True):
    account_number: int | None = Field(
        default=None,
        primary_key=True
    )
    owner_id: int = Field(gt=0) #ex: field shows that in this column the name of it will be owner_id and it will hold an int
    account_type: str
    balance: float = Field(default=0, ge=0)
