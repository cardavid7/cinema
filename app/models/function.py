from sqlmodel import SQLModel, Field

class Function(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    movie_id: int = Field(nullable=False)
    room_id: int = Field(nullable=False)
    start_time: str = Field(nullable=False)
    end_time: str = Field(nullable=False)
    price: float = Field(nullable=False)