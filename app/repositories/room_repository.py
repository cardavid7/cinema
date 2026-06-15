from sqlmodel import Session, select
from app.models.room import Room, RoomCreate, RoomUpdate

class RoomRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, room_id: int) -> Room | None:
        return self.db.get(Room, room_id)

    def get_all(self) -> list[Room]:
        statement = select(Room)
        results = self.db.exec(statement)
        return results.all()

    def get_by_name(self, name: str) -> Room | None:
        return self.db.exec(select(Room).where(Room.name == name)).first()

    def create(self, room_data: RoomCreate) -> Room:
        db_room = Room.model_validate(room_data)
        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room

    def update(self, room: Room) -> Room:
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room

    def delete(self, room: Room):
        self.db.delete(room)
        self.db.commit()

