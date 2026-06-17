from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.movie import Movie
from app.models.room import Room

class Function(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movie.id", index=True, nullable=False)
    room_id: int = Field(foreign_key="room.id", index=True, nullable=False)
    start_time: str = Field(nullable=False)
    end_time: str = Field(nullable=False)
    price: float = Field(nullable=False)

    movie: Optional[Movie] = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    room: Optional[Room] = Relationship(sa_relationship_kwargs={"lazy": "joined"})

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

class FunctionRead(SQLModel):
    id: int
    movie_id: int
    room_id: int
    start_time: str
    end_time: str
    price: float
    movie: Optional[Movie] = None
    room: Optional[Room] = None