from sqlmodel import SQLModel, Field
from typing import Optional

class Seat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    room_id: int = Field(foreign_key="room.id", index=True, nullable=False)
    seat_number: str = Field(index=True, nullable=False)
    is_vip: bool = Field(default=False)
    