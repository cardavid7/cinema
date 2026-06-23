from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, user: UserLogin) -> User:
        if self.user_repo.get_by_email(user.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user.email} already exists")

        new_user = User(
            username=user.email, 
            email=user.email, 
            hashed_password=hash_password(user.password),
            is_active=True
            )
            
        return self.user_repo.create(new_user)

    def login(self, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password[:72], user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

        token = create_access_token(user.id)
        return token