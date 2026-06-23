
from fastapi import APIRouter, Depends, status
from pydantic import EmailStr
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User, UserRead, UserLogin
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.api.depends import DBSession

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_data: UserLogin, db: DBSession) -> User:
    service = AuthService(UserRepository(db))
    return service.register(user_data)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(email: EmailStr, password: str, db: DBSession):
    service = AuthService(UserRepository(db))
    token = service.login(email, password)

    return {"access_token": token, "token_type": "bearer"}

@router.post("/token", status_code=status.HTTP_200_OK)
def token(db: DBSession, form: OAuth2PasswordRequestForm = Depends()):
    email = form.username
    password = form.password
    service = AuthService(UserRepository(db))
    token = service.login(email, password)
    
    return {"access_token": token, "token_type": "bearer"}