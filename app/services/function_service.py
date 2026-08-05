
from datetime import timedelta, datetime
from sqlmodel import Session
from fastapi import HTTPException, status

from app.models.function import Function, FunctionCreate, FunctionUpdate
from app.repositories.function_repository import FunctionRepository
from app.repositories.movie_repository import MovieRepository
from app.repositories.room_repository import RoomRepository

class FunctionService:
    def __init__(self, db: Session):
        self.funtion_repo = FunctionRepository(db)
        self.movie_repo = MovieRepository(db)
        self.room_repo = RoomRepository(db)

    def get_by_id(self, function_id: int) -> Function:
        function = self.funtion_repo.get_by_id(function_id)
        if function is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Function with ID {function_id} not found")
        return function

    def get_all(self) -> list[Function]:
        return self.funtion_repo.get_all()

    def get_all_by_movie_id(self, movie_id: int) -> list[Function]:
        functions = self.funtion_repo.get_all_by_movie_id(movie_id)
        if not functions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Functions with movie ID {movie_id} not found")
        return functions
    
    def get_all_by_room_id(self, room_id: int) -> list[Function]:
        functions = self.funtion_repo.get_all_by_room_id(room_id)
        if not functions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Functions with room ID {room_id} not found")
        return functions

    def create(self, function_data: FunctionCreate) -> Function:
        movie = self.movie_repo.get_by_id(function_data.movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {function_data.movie_id} not found")
        
        room = self.room_repo.get_by_id(function_data.room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with ID {function_data.room_id} not found")
        
        try:
            start_time = datetime.fromisoformat(function_data.start_time)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid start_time format. Must be an ISO 8601 string.")
            
        end_time = start_time + timedelta(minutes=movie.duration)
        
        start_time_str = start_time.isoformat()
        end_time_str = end_time.isoformat()

        # Check for overlapping functions in the same room
        overlapping_function = self.funtion_repo.get_overlapping_function_in_room(
            room_id=function_data.room_id,
            start_time=start_time_str,
            end_time=end_time_str
        )
        if overlapping_function:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The room is already occupied by another function from {overlapping_function.start_time} to {overlapping_function.end_time}"
            )

        db_function = Function(
            movie_id=function_data.movie_id,
            room_id=function_data.room_id,
            start_time=start_time_str,
            end_time=end_time_str,
            price=function_data.price
        )
        return self.funtion_repo.create(db_function)

    def update(self, function_id: int, function_data: FunctionUpdate):
        function = self.funtion_repo.get_by_id(function_id)
        if function is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Function with ID {function_id} not found")
        
        movie = self.movie_repo.get_by_id(function_data.movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID {function_data.movie_id} not found")
        
        room = self.room_repo.get_by_id(function_data.room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with ID {function_data.room_id} not found")
        
        try:
            start_time = datetime.fromisoformat(function_data.start_time)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid start_time format. Must be an ISO 8601 string.")
            
        end_time = start_time + timedelta(minutes=movie.duration)
        
        start_time_str = start_time.isoformat()
        end_time_str = end_time.isoformat()

        # Check for overlapping functions in the same room, excluding the current function
        overlapping_function = self.funtion_repo.get_overlapping_function_in_room(
            room_id=function_data.room_id,
            start_time=start_time_str,
            end_time=end_time_str,
            exclude_id=function_id
        )
        if overlapping_function:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The room is already occupied by another function from {overlapping_function.start_time} to {overlapping_function.end_time}"
            )

        function.movie_id = function_data.movie_id
        function.room_id = function_data.room_id
        function.start_time = start_time_str
        function.end_time = end_time_str
        function.price = function_data.price
        return self.funtion_repo.update(function)

    def delete(self, function_id: int):
        function = self.funtion_repo.get_by_id(function_id)
        if function is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Function with ID {function_id} not found")
        self.funtion_repo.delete(function)
        return True

