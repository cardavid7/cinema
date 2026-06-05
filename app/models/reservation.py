from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime

class ReservationStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class Reservation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False)
    function_id: int = Field(nullable=False)
    seat_id: int = Field(nullable=False)
    status: ReservationStatus = Field(nullable=False)
    created_at: str = Field(default=str(datetime.now()))
    updated_at: str = Field(default=str(datetime.now()))