import os

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from main import app
from database import get_session
from dto.user_db import UserDB


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL must be set before running tests"
    )


test_engine = create_engine(TEST_DATABASE_URL)


def get_test_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_session

client = TestClient(app)


def setup_module():
    SQLModel.metadata.create_all(test_engine)


def teardown_module():
    SQLModel.metadata.drop_all(test_engine)


def test_create_customer_in_database():
    response = client.post(
        "/users",
        json={
            "pin": 2222,
            "is_admin": False
        }
    )

    assert response.status_code == 201

    user_id = response.json()["id"]

    with Session(test_engine) as session:
        db_user = session.get(
            UserDB,
            user_id
        )

        assert db_user is not None
        assert db_user.pin == 2222
        assert db_user.role == "Customer"