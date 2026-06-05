from app.core.db import init_db, engine
from sqlmodel import Session, select
from app.models.reservation import Reservation


def seed_reservation():
    init_db()

    reservations_data = [
        {"user_id":1, "function_id":1, "seat_id":1, "status":"CONFIRMED"},
        {"user_id":1, "function_id":1, "seat_id":2, "status":"CONFIRMED"},
        {"user_id":1, "function_id":1, "seat_id":3, "status":"CONFIRMED"},
        {"user_id":1, "function_id":1, "seat_id":4, "status":"CONFIRMED"},
        {"user_id":1, "function_id":1, "seat_id":5, "status":"CONFIRMED"},
        {"user_id":1, "function_id":1, "seat_id":6, "status":"CONFIRMED"},

        {"user_id":1, "function_id":2, "seat_id":1, "status":"CONFIRMED"},
        {"user_id":1, "function_id":2, "seat_id":2, "status":"CONFIRMED"},
        {"user_id":1, "function_id":2, "seat_id":3, "status":"CONFIRMED"},
        {"user_id":1, "function_id":2, "seat_id":4, "status":"CONFIRMED"},
        {"user_id":1, "function_id":2, "seat_id":5, "status":"CONFIRMED"},
        {"user_id":1, "function_id":2, "seat_id":6, "status":"CONFIRMED"},
    ]

    print("Starting seed of reservations...")

    with Session(engine) as session:
        for r_data in reservations_data:
            statement = select(Reservation).where(Reservation.function_id == r_data["function_id"]).where(Reservation.user_id == r_data["user_id"]).where(Reservation.seat_id == r_data["seat_id"])
            existing_reservation = session.exec(statement).first()
            if not existing_reservation:
                reservation = Reservation(function_id=r_data["function_id"], user_id=r_data["user_id"], seat_id=r_data["seat_id"], status=r_data["status"])
                session.add(reservation)
                print(f"-----> Creating reservation: {r_data['function_id']} - {r_data['user_id']} - {r_data['seat_id']} - {r_data['status']}")
            else:
                print(f"-----> Reservation {r_data['function_id']} - {r_data['user_id']} - {r_data['seat_id']} - {r_data['status']} already exists. Skipping.")

        session.commit()
    print("Seed of Reservation completed successfully!")

if __name__ == "__main__":
    seed_reservation()