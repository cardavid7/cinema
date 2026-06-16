from sqlmodel import SQLModel, Field
from typing import Optional

class Function(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movie.id", index=True, nullable=False)
    room_id: int = Field(foreign_key="room.id", index=True, nullable=False)
    start_time: str = Field(nullable=False)
    end_time: str = Field(nullable=False)
    price: float = Field(nullable=False)

class FunctionCreate(SQLModel):
    movie_id: int 
    room_id: int 
    start_time: str 
    price: float 

class FunctionUpdate(SQLModel):
    movie_id: int
    room_id: int 
    start_time: str
    price: float