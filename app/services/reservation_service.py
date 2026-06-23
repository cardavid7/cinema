from sqlmodel import Session
from fastapi import HTTPException, status
from datetime import datetime

from app.repositories.reservation_repository import ReservationRepository
from app.repositories.function_repository import FunctionRepository
from app.repositories.seat_repository import SeatRepository
from app.repositories.user_repository import UserRepository
from app.models.reservation import Reservation, ReservationCreate, ReservationUpdate, ReservationRead

class ReservationService:
    def __init__(self, db: Session):
        self.reservation_repo = ReservationRepository(db)
        self.function_repo = FunctionRepository(db)
        self.seat_repo = SeatRepository(db)
        self.user_repo = UserRepository(db)

    def get_by_id(self, reservation_id: int) -> Reservation:
        reservation = self.reservation_repo.get_by_id(reservation_id)
        if reservation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reservation with ID {reservation_id} not found")
        return reservation

    def get_by_user_id(self, user_id: int) -> list[Reservation]:
        reservations = self.reservation_repo.get_by_user_id(user_id)
        if not reservations:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reservations with user ID {user_id} not found")
        return reservations

    def get_by_function_id(self, function_id: int) -> list[Reservation]:
        reservations = self.reservation_repo.get_by_function_id(function_id)
        if not reservations:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reservations with function ID {function_id} not found")
        return reservations

    def create(self, reservation_data: ReservationCreate, user_id: int) -> Reservation:
        function = self.function_repo.get_by_id(reservation_data.function_id)
        if function is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Function with ID {reservation_data.function_id} not found")
        seat = self.seat_repo.get_by_id(reservation_data.seat_id)
        if seat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Seat with ID {reservation_data.seat_id} not found")
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")

        if seat.room_id != function.room_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Seat is not in the same room as the function")
        
        # Check if the seat is already reserved for the same function
        existing_reservation = self.reservation_repo.get_reservation_by_seat_and_function_reserved(
            seat_id=reservation_data.seat_id, 
            function_id=reservation_data.function_id
        )
        if existing_reservation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Seat {reservation_data.seat_id} is already reserved for function {reservation_data.function_id}"
            )
        
        db_reservation = Reservation(
            user_id=user_id,
            function_id=reservation_data.function_id,
            seat_id=reservation_data.seat_id,
            status=reservation_data.status,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        return self.reservation_repo.create(db_reservation)

    def update(self, reservation_id: int, reservation_data: ReservationUpdate):

        reservation = self.reservation_repo.get_by_id(reservation_id)
        if reservation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reservation with ID {reservation_id} not found")
        
        existing_reservation = self.reservation_repo.get_reservation_by_seat_and_function_reserved(
            seat_id=reservation.seat_id, 
            function_id=reservation.function_id
        )
        if existing_reservation and reservation_id != existing_reservation.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Seat {reservation.seat_id} is already reserved for function {reservation.function_id}"
            )

        reservation.status = reservation_data.status
        reservation.updated_at = datetime.now().isoformat()
        return self.reservation_repo.update(reservation)

    def delete(self, reservation_id: int):
        reservation = self.reservation_repo.get_by_id(reservation_id)
        if reservation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reservation with ID {reservation_id} not found")
        self.reservation_repo.delete(reservation)
        return True

    