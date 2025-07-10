from fastapi import APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Any
from backend.core.deps import SessionDep, CurrentUser
from fastapi import Depends
from backend.models.models import Token, UserPublic, NewPassword, Message
from backend.core.crud import authenticate
from datetime import timedelta
from backend.config.config import settings
from backend.core.security import create_access_token

from backend.core.crud import get_user_by_email


router = APIRouter(tags=["login"])


@router.post("/login/access-token", status_code=status.HTTP_200_OK)
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(
        access_token=create_access_token(user.id, expires_delta=access_token_expires)
    )


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password():
    return {"message": "recover_password"}


@router.post("/reset-password/")
def reset_password() -> Message:
    return {"message": "reset password"}


@router.post("/password-recovery-html-content/{email}")
def recover_password_html_content():
    return {"message": "recover_password_html_content"}
