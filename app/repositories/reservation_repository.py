from sqlmodel import Session, select
from app.models.reservation import Reservation, ReservationStatus

class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, reservation_id: int):
        return self.db.get(Reservation, reservation_id)

    def get_by_user_id(self, user_id: int):
        return self.db.exec(select(Reservation).where(Reservation.user_id == user_id)).all()

    def get_by_function_id(self, function_id: int):
        return self.db.exec(select(Reservation).where(Reservation.function_id == function_id)).all()

    def get_reservation_by_seat_and_function_reserved(self, seat_id: int, function_id: int):
        return self.db.exec(select(Reservation).where(
            Reservation.seat_id == seat_id, 
            Reservation.function_id == function_id,
            Reservation.status == ReservationStatus.CONFIRMED
        )).first()

    def create(self, reservation: Reservation):
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def update(self, reservation: Reservation):
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def delete(self, reservation: Reservation):
        self.db.delete(reservation)
        self.db.commit()