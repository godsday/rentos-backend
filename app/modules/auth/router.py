from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.repository import UserRepository
from fastapi.security import OAuth2PasswordRequestForm

form_data: OAuth2PasswordRequestForm = Depends()

from app.modules.auth.schema import (
    CreateUserRequest,
    UserResponse,
)
from app.modules.auth.service import UserService
from app.modules.auth.schema import TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

from app.core.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.auth.schema import CurrentUserResponse


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = UserService(repository)

    return service.register(request)




from app.modules.auth.schema import (
    LoginRequest,
    TokenResponse,
)

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = UserService(repository)

    return service.login(
        form_data.username,   # username = email
        form_data.password,
    )

@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


