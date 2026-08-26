import os

<<<<<<< HEAD
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from models.account_model import AccountRecord
from dto.user_db import UserDB


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL must be set before starting the application"
    )


engine = create_engine(DATABASE_URL)
=======
from fastapi import Depends #this is going to tell fastapi that we want to use the results from another function before we run the function we are currently in. We will be using it to get our database session before running our routers
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy import text

from models.account_model import AccountRecord #imports the account table model we made so SQLModel knows the layout when creating our database tables

#assigns our database url to DATABASE_URL using os to grab it from the environmant variables in the terminal, raises an error if not set
# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise RuntimeError(
#         "DATABASE_URL must be set before starting the application"
#     )
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///banking.db")
#an engine is just a connection manager. It will know what database to connect to, which driver to use, how to open the connections for the databse, and how to manage and reuse those connections.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
>>>>>>> origin/main


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    if not DATABASE_URL.startswith("sqlite"):
        with engine.begin() as connection:
            connection.execute(text(
                "ALTER TABLE transaction ALTER COLUMN category DROP NOT NULL"
            ))


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[
    Session,
    Depends(get_session)
]