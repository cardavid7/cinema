from sqlmodel import SQLModel, Field
from typing import Optional

class Seat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    room_id: int = Field(foreign_key="room.id", index=True, nullable=False)
    seat_number: str = Field(index=True, nullable=False)
    is_vip: bool = Field(default=False)

class SeatCreate(SQLModel):
    room_id: int
    seat_number: str
    is_vip: bool

class SeatUpdate(SQLModel):
    room_id: Optional[int] = None
    seat_number: Optional[str] = None
    is_vip: Optional[bool] = None