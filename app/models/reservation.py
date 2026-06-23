from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime
from typing import Optional
from app.models.user import User
from app.models.function import Function
from app.models.seat import Seat

class ReservationStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True, nullable=False)
    function_id: int = Field(foreign_key="function.id", index=True, nullable=False)
    seat_id: int = Field(foreign_key="seat.id", index=True, nullable=False)
    status: ReservationStatus = Field(nullable=False)
    created_at: str = Field(default=str(datetime.now()))
    updated_at: str = Field(default=str(datetime.now()))

    user: Optional[User] = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    function: Optional[Function] = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    seat: Optional[Seat] = Relationship(sa_relationship_kwargs={"lazy": "joined"})

class ReservationCreate(SQLModel):
    function_id: int
    seat_id: int
    status: ReservationStatus

class ReservationUpdate(SQLModel):
    status: ReservationStatus

class ReservationRead(SQLModel):
    id: int
    user_id: int
    function_id: int
    seat_id: int
    status: ReservationStatus
    created_at: str
    updated_at: str
    user: Optional[User] = None
    function: Optional[Function] = None
    seat: Optional[Seat] = None