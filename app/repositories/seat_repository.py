
from sqlmodel import Session, select

from app.models.seat import Seat

class SeatRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, seat_id: int) -> Seat | None:
        return self.db.get(Seat, seat_id)

    def get_by_room_id(self, room_id: int) -> list[Seat]:
        return self.db.exec(select(Seat).where(Seat.room_id == room_id).order_by(Seat.seat_number.asc())).all()

    def get_by_room_id_and_seat_number(self, room_id: int, seat_number: str) -> Seat | None:
        return self.db.exec(select(Seat).where(Seat.room_id == room_id, Seat.seat_number == seat_number)).first()

    def create(self, seat: Seat):
        self.db.add(seat)
        self.db.commit()
        self.db.refresh(seat)
        return seat

    def update(self, seat: Seat):
        self.db.add(seat)
        self.db.commit()
        self.db.refresh(seat)
        return seat
    
    def delete(self, seat: Seat):
        self.db.delete(seat)
        self.db.commit()

    def delete_all_by_room_id(self, room_id: int):
        seats = self.get_by_room_id(room_id)
        for seat in seats:
            self.db.delete(seat)
            self.db.commit()

