from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: EmailStr = Field(index=True, nullable=False, unique=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    role: UserRole = Field(default=UserRole.USER, nullable=False)

class UserCreate(SQLModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(SQLModel):
    username: str
    email: EmailStr
    password: str
    is_active: bool

class UserRead(SQLModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    role: UserRole

class UserLogin(SQLModel):
    email: EmailStr
    password: str
