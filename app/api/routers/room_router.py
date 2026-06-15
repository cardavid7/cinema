from fastapi import APIRouter
from typing import List

from app.models.room import Room, RoomCreate, RoomUpdate
from app.api.depends import DBSession
from app.services.room_service import RoomService

router = APIRouter(prefix='/rooms', tags=['Rooms'])

@router.get("/", response_model=List[Room], status_code=200)
def list_rooms(db: DBSession):
    service = RoomService(db)
    return service.get_all()

@router.get("/{room_id}", response_model=Room, status_code=200)
def get_room_by_id(db: DBSession, room_id: int):
    service = RoomService(db)
    return service.get_by_id(room_id)

@router.post("/", response_model=Room, status_code=201)
def create_room(db: DBSession, room: RoomCreate):
    service = RoomService(db)
    return service.create(room)

@router.put("/{room_id}", response_model=Room, status_code=200)
def update_room(db: DBSession, room_id: int, room: RoomUpdate):
    service = RoomService(db)
    return service.update(room_id, room)

@router.delete("/{room_id}", status_code=204)
def delete_room(db: DBSession, room_id: int):
    service = RoomService(db)
    return service.delete(room_id)