from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from data import ACCOUNTS, USERS

router = APIRouter()


class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    is_admin: bool = False


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    is_admin: bool | None = None


def _find_user(user_id: int):
    for user in USERS:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@router.get("")
def list_users():
    return {"users": USERS}


@router.get("/{user_id}")
def read_user(user_id: int):
    return _find_user(user_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user_request: UserCreate):
    user = {
        "id": max((user["id"] for user in USERS), default=0) + 1,
        "name": user_request.name,
        "is_admin": user_request.is_admin,
    }
    USERS.append(user)
    return user


@router.patch("/{user_id}")
def update_user(user_id: int, user_request: UserUpdate):
    user = _find_user(user_id)
    if user_request.name is not None:
        user["name"] = user_request.name
    if user_request.is_admin is not None:
        user["is_admin"] = user_request.is_admin
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int):
    user = _find_user(user_id)
    if any(account["owner_id"] == user_id for account in ACCOUNTS):
        raise HTTPException(status_code=400, detail="User still owns one or more accounts")
    USERS.remove(user)
    return {"user_id": user_id, "deleted": True}