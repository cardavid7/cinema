from sqlmodel import Session, select
from app.core.db import init_db, engine
from app.models.room import Room
from app.models.seat import Seat, SeatCreate
from app.services.seat_service import SeatService
from fastapi import HTTPException

def seed_seat():
    init_db()

    # Mapping of room name to generation rules: List of (row_letter, col_count, is_vip)
    generation_rules = {
        "Room 1 (General)": [("A", 5, False), ("B", 5, False)],
        "Room 2 (IMAX 3D)": [("A", 5, False), ("B", 5, False), ("C", 5, True)],
        "Room 3 (2D / 3D)": [("A", 4, False), ("B", 4, False)],
        "Room VIP": [("V", 4, True)],
        "Room Premium 4D": [("A", 6, False), ("B", 6, True)],
    }

    print("Starting seed of seats...")

    with Session(engine) as session:
        seat_service = SeatService(session)
        
        # Get all rooms in the database
        rooms = session.exec(select(Room)).all()
        if not rooms:
            print("###### Error: No rooms found in the database. Please run room seeder first!")
            return

        for room in rooms:
            rules = generation_rules.get(room.name)
            if not rules:
                print(f"No seat generation rules defined for room: '{room.name}'. Skipping.")
                continue
            
            print(f"Generating seats for room: '{room.name}' (ID: {room.id}, Capacity: {room.capacity})...")
            
            for row, cols, is_vip in rules:
                for col in range(1, cols + 1):
                    seat_num = f"{row}{col}"
                    seat_create = SeatCreate(
                        room_id=room.id,
                        seat_number=seat_num,
                        is_vip=is_vip
                    )
                    
                    # Check if seat already exists in room
                    statement = select(Seat).where(Seat.room_id == room.id, Seat.seat_number == seat_num)
                    existing_seat = session.exec(statement).first()
                    
                    if not existing_seat:
                        try:
                            seat_service.create(seat_create)
                            print(f"-----> Creating seat: Room '{room.name}' - Seat {seat_num} (VIP: {is_vip})")
                        except HTTPException as e:
                            print(f"###### Error creating seat {seat_num}: {e.detail}")
                    else:
                        print(f"-----> Seat {seat_num} in room '{room.name}' already exists. Skipping.")
        
        session.commit()
    print("Seed of Seat completed successfully!")

if __name__ == "__main__":
    seed_seat()