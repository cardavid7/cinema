from fastapi import HTTPException, status
from sqlmodel import Session

from app.repositories.room_repository import RoomRepository
from app.models.room import Room, RoomCreate, RoomUpdate

class RoomService:
    def __init__(self, db: Session):
        self.room_repo = RoomRepository(db)
    
    def get_all(self):
        return self.room_repo.get_all()

    def get_by_id(self, room_id: int):
        room = self.room_repo.get_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        return room

    def create(self, room_data: RoomCreate) -> Room | None:
        existing_room = self.room_repo.get_by_name(room_data.name)
        if existing_room:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Room already exists")
        return self.room_repo.create(room_data)

    def update(self, room_id: int, room_data: RoomUpdate):
        room = self.room_repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

        if room.name != room_data.name:
            existing_room = self.room_repo.get_by_name(room_data.name)
            if existing_room:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Room already exists")

        room.name = room_data.name if room_data.name is not None else room.name
        room.capacity = room_data.capacity if room_data.capacity is not None else room.capacity
        return self.room_repo.update(room)

    def delete(self, room_id: int):
        room = self.room_repo.get_by_id(room_id)
        if not room:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        self.room_repo.delete(room)
        return True