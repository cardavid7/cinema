from sqlmodel import Session
from fastapi import HTTPException, status

from app.models.user import User, UserCreate, UserUpdate
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def get_by_id(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
        return user

    def get_by_username(self, username: str) -> User:
        user = self.user_repo.get_by_username(username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
        return user

    def get_by_email(self, email: str) -> User:
        user = self.user_repo.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
        return user

    def create(self, user_data: UserCreate) -> User:
        if self.user_repo.get_by_email(user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user_data.email} already exists")
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=user_data.password,
            is_active=True
        )
        return self.user_repo.create(user)

    def update(self, user_id: int, user_data: UserUpdate) -> User:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
        if user_data.email != user.email and self.user_repo.get_by_email(user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user_data.email} already exists")
        user.username = user_data.username
        user.email = user_data.email
        user.hashed_password = user_data.password
        user.is_active = user_data.is_active
        return self.user_repo.update(user)

    def delete(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")
        self.user_repo.delete(user)