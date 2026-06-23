from sqlmodel import Session, select
from app.core.db import engine, init_db
from app.models.room import Room, RoomCreate
from app.services.room_service import RoomService
from fastapi import HTTPException

def seed_rooms():
    init_db()
    
    rooms_data = [
        RoomCreate(name="Room 1 (General)", capacity=10),
        RoomCreate(name="Room 2 (IMAX 3D)", capacity=10),
        RoomCreate(name="Room 3 (2D / 3D)", capacity=15),
        RoomCreate(name="Room VIP", capacity=8),
        RoomCreate(name="Room Premium 4D", capacity=12),
    ]
    
    print("Starting seed of rooms...")
    
    with Session(engine) as session:
        service = RoomService(session)
        for r_data in rooms_data:
            statement = select(Room).where(Room.name == r_data.name)
            existing_room = session.exec(statement).first()
            
            if not existing_room:
                try:
                    service.create(r_data)
                    print(f"-----> Creating room: {r_data.name} (Capacity: {r_data.capacity})")
                except HTTPException as e:
                    print(f"###### Error creating room {r_data.name}: {e.detail}")
            else:
                print(f"-----> Room '{r_data.name}' already exists. Skipping.")
                
        session.commit()
    print("Seed of Room completed successfully!")

if __name__ == "__main__":
    seed_rooms()
