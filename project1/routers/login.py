from fastapi import APIRouter, HTTPException

from database import SessionDep
from dto.login_request import LoginRequest
from service import user_service

router = APIRouter()


@router.post("")
def login(
    request: LoginRequest,
    session: SessionDep
):
    try:
        token = user_service.authenticate(
            session,
            request.email,
            request.password
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error)
        )