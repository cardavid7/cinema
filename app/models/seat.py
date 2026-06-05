from sqlmodel import SQLModel, Field

class Seat(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    room_id: int = Field(nullable=False)
    seat_row: str = Field(nullable=False)
    seat_number: int = Field(nullable=False)
    is_vip: bool = Field(default=False)
    