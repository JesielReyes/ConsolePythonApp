from sqlmodel import SQLModel, Field


class UserDB(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    pin: int

    role: str