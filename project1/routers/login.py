from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session

from database import get_session
from service import user_service


router = APIRouter()

class LoginRequest(BaseModel):
	email: EmailStr
	password: str = Field(min_length=1)


class LoginResponse(BaseModel):
	message: str
	user_id: UUID
	first_name: str
	is_admin: bool
	redirect_to: str


def user_to_login_response(user) -> LoginResponse:
	is_admin = user.get_role() == "Admin"
	target_ui = "/admin-dashboard" if is_admin else "/user-dashboard"

	return LoginResponse(
		message="Login successful",
		user_id=user.get_owner_id(),
		first_name=user.first_name,
		is_admin=is_admin,
		redirect_to=target_ui,
	)


@router.post(
	"/login",
	response_model=LoginResponse,
	status_code=status.HTTP_200_OK,
)
def login(
	credentials: LoginRequest,
	session: Annotated[Session, Depends(get_session)],
):
	try:
		user = user_service.authenticate_user(
			session=session,
			email=str(credentials.email),
			password=credentials.password,
		)

		return user_to_login_response(user)

	except ValueError as error:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=str(error),
		) from error
