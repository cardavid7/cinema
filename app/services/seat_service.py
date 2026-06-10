from sqlmodel import Session
from fastapi import HTTPException, status

from app.models.seat import Seat
from app.repositories.seat_repository import SeatRepository

class SeatService:
    def __init__(self, db: Session):
        self.seat_repo = SeatRepository(db)

    def get_by_id(self, seat_id: int) -> Seat:
        seat = self.seat_repo.get_by_id(seat_id)
        if seat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Seat with ID {seat_id} not found")
        return seat
    
    def get_by_room_id(self, room_id: int) -> list[Seat]:
        return self.seat_repo.get_by_room_id(room_id)
    
    def create(self, seat: Seat) -> Seat:
        return self.seat_repo.create(seat)
    
    def update(self, seat_id: int, seat_data: Seat) -> Seat:
        seat = self.seat_repo.get_by_id(seat_id)
        if seat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Seat with ID {seat_id} not found")
        seat.room_id = seat_data.room_id
        seat.seat_number = seat_data.seat_number
        seat.is_vip = seat_data.is_vip
        return self.seat_repo.update(seat)
    
    def delete(self, seat_id: int) -> bool:
        seat = self.seat_repo.get_by_id(seat_id)
        if seat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Seat with ID {seat_id} not found")
        self.seat_repo.delete(seat)
        return True
    
    def delete_all_by_room_id(self, room_id: int):
        seats = self.seat_repo.get_by_room_id(room_id)
        if not seats:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Seats with room ID {room_id} not found")
        self.seat_repo.delete_all_by_room_id(room_id)