
from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional

class MovieFormat(str, Enum):
    TWO_D = "2D"
    TWO_D_SUB = "2D_SUB"
    THREE_D = "3D"
    THREE_D_SUB = "3D_SUB"

class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    description: str = Field(nullable=False)
    duration: int = Field(nullable=False)
    format: MovieFormat = Field(nullable=False)

class MovieCreate(SQLModel):
    title: str
    description: str
    duration: int
    format: MovieFormat

class MovieUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    format: Optional[MovieFormat] = None