from sqlmodel import Session
from fastapi import HTTPException, status

from app.models.seat import Seat, SeatCreate, SeatUpdate
from app.repositories.seat_repository import SeatRepository
from app.repositories.room_repository import RoomRepository

class SeatService:
    def __init__(self, db: Session):
        self.seat_repo = SeatRepository(db)
        self.room_repo = RoomRepository(db)

    def get_by_id(self, seat_id: int) -> Seat:
        seat = self.seat_repo.get_by_id(seat_id)
        if seat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Seat with ID {seat_id} not found")
        return seat
    
    def get_by_room_id(self, room_id: int) -> list[Seat]:
        return self.seat_repo.get_by_room_id(room_id)
    
    def create(self, seat: SeatCreate) -> Seat:
        room = self.room_repo.get_by_id(seat.room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with ID {seat.room_id} not found")

        existing_seat = self.seat_repo.get_by_room_id_and_seat_number(seat.room_id, seat.seat_number)
        if existing_seat:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Seat '{seat.seat_number}' already exists in room '{seat.room_id}'")

        return self.seat_repo.create(seat)
    
    def update(self, seat_id: int, seat_data: SeatUpdate) -> Seat:
        if seat_data.room_id:
            room = self.room_repo.get_by_id(seat_data.room_id)
            if room is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with ID {seat_data.room_id} not found")

        seat = self.seat_repo.get_by_id(seat_id)
        if seat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Seat with ID {seat_id} not found")

        if seat.room_id != seat_data.room_id or seat.seat_number != seat_data.seat_number:
            existing_seat = self.seat_repo.get_by_room_id_and_seat_number(seat_data.room_id, seat_data.seat_number)
            if existing_seat:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Seat '{seat_data.seat_number}' already exists in room '{seat_data.room_id}'")

        seat.room_id = seat_data.room_id if seat_data.room_id is not None else seat.room_id
        seat.seat_number = seat_data.seat_number if seat_data.seat_number is not None else seat.seat_number
        seat.is_vip = seat_data.is_vip if seat_data.is_vip is not None else seat.is_vip
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