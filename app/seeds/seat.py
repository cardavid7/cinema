from sqlmodel import Session, select
from app.core.db import init_db, engine
from app.models.seat import Seat

def seed_seat():
    # Starting database tables creation
    init_db()

    seats_data = [
        {"room_id": 1, "seat_number": "A1", "is_vip": False},
        {"room_id": 1, "seat_number": "A2", "is_vip": False},
        {"room_id": 1, "seat_number": "A3", "is_vip": False},
        {"room_id": 1, "seat_number": "B1", "is_vip": False},
        {"room_id": 1, "seat_number": "B2", "is_vip": False},
        {"room_id": 1, "seat_number": "B3", "is_vip": False},
        {"room_id": 1, "seat_number": "C1", "is_vip": True},
        {"room_id": 1, "seat_number": "C2", "is_vip": True},
        {"room_id": 1, "seat_number": "C3", "is_vip": True},
        {"room_id": 1, "seat_number": "D1", "is_vip": True},
    ]

    print("Starting seed of seat...")

    with Session(engine) as session:
        for s_data in seats_data:
            statement = select(Seat).where(Seat.room_id == s_data["room_id"], Seat.seat_number == s_data["seat_number"])
            existing_seat = session.exec(statement).first()

            if not existing_seat:
                seat = Seat(room_id=s_data["room_id"], seat_number=s_data["seat_number"], is_vip=s_data["is_vip"])
                session.add(seat)
                print(f"-----> Creating seat: {s_data['seat_number']}, is_vip: {s_data['is_vip']}")
            else:
                print(f"-----> Seat '{s_data['seat_number']}' already exists. Skipping.")
        
        session.commit()
        print("Seed of Seat completed successfully!")

if __name__ == "__main__":
    seed_seat()