from sqlmodel import Session, select
from app.core.db import init_db, engine
from app.models.user import User
from app.models.movie import Movie
from app.models.room import Room
from app.models.seat import Seat
from app.models.function import Function
from app.models.reservation import Reservation, ReservationCreate, ReservationStatus
from app.services.reservation_service import ReservationService
from fastapi import HTTPException

def seed_reservation():
    init_db()

    print("Starting seed of reservations...")

    # Bookings specification: (user_email, movie_title, movie_format, room_name, start_time, seat_number, status)
    bookings_to_seed = [
        # Bookings for Room 1 (General) - Iron Man
        ("user@email.com", "Iron Man", "2D_SUB", "Room 1 (General)", "2026-06-25T10:00:00", "A1", ReservationStatus.CONFIRMED),
        ("juan@email.com", "Iron Man", "2D_SUB", "Room 1 (General)", "2026-06-25T10:00:00", "A2", ReservationStatus.CONFIRMED),
        ("maria@email.com", "Iron Man", "2D_SUB", "Room 1 (General)", "2026-06-25T10:00:00", "A3", ReservationStatus.CONFIRMED),
        
        # Bookings for Room VIP - The Dark Knight
        ("juan@email.com", "The Dark Knight", "2D", "Room VIP", "2026-06-25T14:00:00", "V1", ReservationStatus.CONFIRMED),
        ("maria@email.com", "The Dark Knight", "2D", "Room VIP", "2026-06-25T14:00:00", "V2", ReservationStatus.CONFIRMED),
        ("carlos@email.com", "The Dark Knight", "2D", "Room VIP", "2026-06-25T14:00:00", "V3", ReservationStatus.CONFIRMED),

        # Bookings for Room Premium 4D - Avatar
        ("user@email.com", "Avatar: The Way of Water", "3D", "Room Premium 4D", "2026-06-25T12:00:00", "A1", ReservationStatus.CONFIRMED),
        ("maria@email.com", "Avatar: The Way of Water", "3D", "Room Premium 4D", "2026-06-25T12:00:00", "B1", ReservationStatus.CONFIRMED),
        
        # Bookings for Room 2 (IMAX 3D) - Thor
        ("carlos@email.com", "Thor: Ragnarok", "2D_SUB", "Room 2 (IMAX 3D)", "2026-06-25T10:00:00", "A1", ReservationStatus.CONFIRMED),
        ("juan@email.com", "Thor: Ragnarok", "2D_SUB", "Room 2 (IMAX 3D)", "2026-06-25T10:00:00", "B1", ReservationStatus.CONFIRMED),
    ]

    with Session(engine) as session:
        reservation_service = ReservationService(session)

        for user_email, movie_title, movie_format, room_name, start_time, seat_num, status in bookings_to_seed:
            # 1. Resolve User
            user_stmt = select(User).where(User.email == user_email)
            user = session.exec(user_stmt).first()
            if not user:
                print(f"###### Error: User '{user_email}' not found. Skipping booking.")
                continue

            # 2. Resolve Movie
            movie_stmt = select(Movie).where(Movie.title == movie_title, Movie.format == movie_format)
            movie = session.exec(movie_stmt).first()
            if not movie:
                print(f"###### Error: Movie '{movie_title}' ({movie_format}) not found. Skipping booking.")
                continue

            # 3. Resolve Room
            room_stmt = select(Room).where(Room.name == room_name)
            room = session.exec(room_stmt).first()
            if not room:
                print(f"###### Error: Room '{room_name}' not found. Skipping booking.")
                continue

            # 4. Resolve Function
            func_stmt = select(Function).where(
                Function.movie_id == movie.id,
                Function.room_id == room.id,
                Function.start_time == start_time
            )
            function = session.exec(func_stmt).first()
            if not function:
                print(f"###### Error: Function for '{movie_title}' in '{room_name}' at {start_time} not found. Skipping booking.")
                continue

            # 5. Resolve Seat
            seat_stmt = select(Seat).where(
                Seat.room_id == room.id,
                Seat.seat_number == seat_num
            )
            seat = session.exec(seat_stmt).first()
            if not seat:
                print(f"###### Error: Seat '{seat_num}' in Room '{room_name}' not found. Skipping booking.")
                continue

            # 6. Check if reservation already exists
            res_stmt = select(Reservation).where(
                Reservation.function_id == function.id,
                Reservation.seat_id == seat.id,
                Reservation.user_id == user.id
            )
            existing_res = session.exec(res_stmt).first()

            if not existing_res:
                res_create = ReservationCreate(
                    function_id=function.id,
                    seat_id=seat.id,
                    status=status
                )
                try:
                    reservation_service.create(res_create, user.id)
                    print(f"-----> Creating reservation: User '{user_email}' -> Room '{room_name}', Seat {seat_num} for '{movie_title}'")
                except HTTPException as e:
                    print(f"###### Error booking seat {seat_num} for '{user_email}': {e.detail}")
            else:
                print(f"-----> Reservation for user '{user_email}' at seat '{seat_num}' already exists. Skipping.")

        session.commit()
    print("Seed of Reservation completed successfully!")

if __name__ == "__main__":
    seed_reservation()