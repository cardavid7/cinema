from typing import Optional
from sqlmodel import Field, SQLModel


class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False, unique=True)
    capacity: int = Field(nullable=False, ge=1)

class RoomCreate(SQLModel):
    name: str
    capacity: int

class RoomUpdate(SQLModel):
    name: Optional[str] = None
    capacity: Optional[int] = None