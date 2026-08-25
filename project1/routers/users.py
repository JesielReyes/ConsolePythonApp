from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from service import user_service


router = APIRouter()


class UserCreate(BaseModel):
    pin: int = Field(gt=0)
    is_admin: bool = False


def user_to_dict(user):
    return {
        "id": user.get_owner_id(),
        "role": user.get_role()
    }


@router.get("")
def list_users():
    users = user_service.get_all_users()

    return {
        "users": [
            user_to_dict(user)
            for user in users
        ]
    }


@router.get("/{user_id}")
def read_user(user_id: int):
    try:
        user = user_service.get_user(user_id)

        return user_to_dict(user)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user_request: UserCreate):
    try:
        user = user_service.create_user(
            pin=user_request.pin,
            is_admin=user_request.is_admin
        )

        return user_to_dict(user)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.delete("/{user_id}")
def delete_user(user_id: int):
    try:
        user_service.delete_user(user_id)

        return {
            "user_id": user_id,
            "deleted": True
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )