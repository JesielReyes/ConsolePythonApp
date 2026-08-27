from fastapi import APIRouter, HTTPException, status
from datetime import date
from pydantic import BaseModel
from uuid import UUID

from database import SessionDep
from service import user_service


router = APIRouter()


class UserCreate(BaseModel):
    email: str
    password: str
    is_admin: bool = False
    birthday: date
    phone_number: str
    first_name: str
    last_name: str


class LoginRequest(BaseModel):
    email: str
    password: str


def user_to_dict(user):
    return {
        "id": user.get_owner_id(),
        "email": user.email,
        "is_admin": user.get_role() == "Admin",
        "birthday": user.birthday,
        "phone_number": user.phone_number,
        "first_name": user.first_name,
        "last_name": user.last_name
    }


@router.get("")
def list_users(
    session: SessionDep
):
    users = user_service.get_all_users(
        session
    )

    return {
        "users": [
            user_to_dict(user)
            for user in users
        ]
    }


@router.get("/{user_id}")
def read_user(
    user_id: UUID,
    session: SessionDep
):
    try:
        user = user_service.get_user(
            session,
            user_id
        )

        return user_to_dict(user)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_request: UserCreate,
    session: SessionDep
):
    user = user_service.create_user(
        session,
        email=user_request.email, password=user_request.password, is_admin=user_request.is_admin,
        birthday=user_request.birthday, phone_number=user_request.phone_number,
        first_name=user_request.first_name, last_name=user_request.last_name
    )

    return user_to_dict(user)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    session: SessionDep
):
    try:
        user_service.delete_user(
            session,
            user_id
        )

        return {
            "user_id": user_id,
            "deleted": True
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/login")
def login(login_request: LoginRequest, session: SessionDep):
    try:
        user = user_service.authenticate(session, login_request.email, login_request.password)
        return {"user_id": user.id, "is_admin": user.is_admin}
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error))