
from sqlmodel import Session, select

from app.models.function import Function, FunctionCreate

class FunctionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, function_id: int) -> Function | None:
        return self.db.get(Function, function_id)

    def get_all(self) -> list[Function]:
        return self.db.exec(select(Function)).all()

    def get_all_by_movie_id(self, movie_id: int) -> list[Function] | None:
        return self.db.exec(select(Function).where(Function.movie_id == movie_id)).all()

    def get_all_by_room_id(self, room_id: int) -> list[Function] | None:
        return self.db.exec(select(Function).where(Function.room_id == room_id)).all()

    def get_by_movie_id_room_id_and_start_time(self, movie_id: int, room_id: int, start_time: str) -> Function | None:
        return self.db.exec(select(Function).where(Function.movie_id == movie_id, Function.room_id == room_id, Function.start_time <= start_time, Function.end_time >= start_time)).first()
    
    def get_overlapping_function_in_room(self, room_id: int, start_time: str, end_time: str, exclude_id: int | None = None) -> Function | None:
        statement = select(Function).where(
            Function.room_id == room_id,
            Function.start_time < end_time,
            Function.end_time > start_time
        )
        if exclude_id is not None:
            statement = statement.where(Function.id != exclude_id)
        return self.db.exec(statement).first()

    def create(self, function: Function) -> Function:
        self.db.add(function)
        self.db.commit()
        self.db.refresh(function)
        return function

    def update(self, function: Function) -> Function:
        self.db.add(function)
        self.db.commit()
        self.db.refresh(function)
        return function

    def delete(self, function: Function):
        self.db.delete(function)
        self.db.commit()
        