from sqlmodel import Session, select
from app.core.db import engine, init_db
from app.models.room import Room

def seed_rooms():
    # Starting database tables creation
    init_db()
    
    # Initial data for rooms
    rooms_data = [
        {"name": "Room 1 (General)", "capacity": 10},
        {"name": "Room 2 (IMAX 3D)", "capacity": 15},
        {"name": "Room 3 (2D / 3D)", "capacity": 8},
        {"name": "Room VIP", "capacity": 4},
    ]
    
    print("Starting seed of rooms...")
    
    with Session(engine) as session:
        for r_data in rooms_data:
            # Check if room already exists
            statement = select(Room).where(Room.name == r_data["name"])
            existing_room = session.exec(statement).first()
            
            if not existing_room:
                room = Room(name=r_data["name"], capacity=r_data["capacity"])
                session.add(room)
                print(f"-----> Creating room: {r_data['name']} (Capacity: {r_data['capacity']})")
            else:
                print(f"-----> Room '{r_data['name']}' already exists. Skipping.")
                
        session.commit()
    print("Seed of Room completed successfully!")

if __name__ == "__main__":
    seed_rooms()
