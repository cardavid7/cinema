from fastapi import APIRouter
from typing import List

from app.api.depends import DBSession, CurrentUser, AdminUser
from app.models.seat import Seat, SeatCreate, SeatUpdate
from app.services.seat_service import SeatService

router = APIRouter(prefix='/seats', tags=['Seats'])

@router.get("/", response_model=List[Seat], status_code=200)
def list_seats_by_room_id(db: DBSession, room_id: int, user: CurrentUser):
    service = SeatService(db)
    return service.get_by_room_id(room_id)

@router.get("/{seat_id}", response_model=Seat, status_code=200)
def get_seat_by_id(db: DBSession, seat_id: int, user: CurrentUser):
    service = SeatService(db)
    return service.get_by_id(seat_id)

@router.post("/", response_model=Seat, status_code=201)
def create_seat(db: DBSession, seat: SeatCreate, user: AdminUser):
    service = SeatService(db)
    return service.create(seat)

@router.put("/{seat_id}", response_model=Seat, status_code=200)
def update_seat(db: DBSession, seat_id: int, seat: SeatUpdate, user: AdminUser):
    service = SeatService(db)
    return service.update(seat_id, seat)

@router.delete("/{seat_id}", status_code=204)
def delete_seat(db: DBSession, seat_id: int, user: AdminUser):
    service = SeatService(db)
    return service.delete(seat_id)

@router.delete("/room/{room_id}", status_code=204)
def delete_all_seats_by_room_id(db: DBSession, room_id: int, user: AdminUser):
    service = SeatService(db)
    return service.delete_all_by_room_id(room_id)