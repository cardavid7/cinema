from sqlmodel import Session, select
from app.core.db import init_db, engine
from app.models.movie import Movie
from app.models.room import Room
from app.models.function import Function, FunctionCreate
from app.services.function_service import FunctionService
from fastapi import HTTPException

def seed_function():
    init_db()

    print("Starting seed of functions...")

    # Pairings of (movie_title, movie_format, room_name, start_time, price)
    functions_to_seed = [
        # Room 1
        ("Iron Man", "2D_SUB", "Room 1 (General)", "2026-06-25T10:00:00", 10.0),
        ("The Dark Knight", "2D", "Room 1 (General)", "2026-06-25T13:00:00", 12.0),
        ("Spider-Man: Into the Spider-Verse", "2D", "Room 1 (General)", "2026-06-25T16:00:00", 10.0),
        ("Avengers: Infinity War", "3D", "Room 1 (General)", "2026-06-25T19:00:00", 15.0),
        
        # Room 2
        ("Thor: Ragnarok", "2D_SUB", "Room 2 (IMAX 3D)", "2026-06-25T10:00:00", 12.0),
        ("Avatar: The Way of Water", "3D", "Room 2 (IMAX 3D)", "2026-06-25T13:00:00", 18.0),
        ("Inception", "2D_SUB", "Room 2 (IMAX 3D)", "2026-06-25T17:00:00", 14.0),
        ("Interstellar", "2D_SUB", "Room 2 (IMAX 3D)", "2026-06-25T20:00:00", 14.0),
        
        # Room 3
        ("Captain America: The First Avenger", "2D", "Room 3 (2D / 3D)", "2026-06-25T10:00:00", 8.0),
        ("Captain Marvel", "3D_SUB", "Room 3 (2D / 3D)", "2026-06-25T13:00:00", 10.0),
        ("Iron Man", "2D_SUB", "Room 3 (2D / 3D)", "2026-06-26T10:00:00", 8.0),
        
        # Room VIP
        ("The Dark Knight", "2D", "Room VIP", "2026-06-25T14:00:00", 25.0),
        ("Inception", "2D_SUB", "Room VIP", "2026-06-25T18:00:00", 25.0),
        
        # Room Premium 4D
        ("Avatar: The Way of Water", "3D", "Room Premium 4D", "2026-06-25T12:00:00", 22.0),
        ("Avengers: Infinity War", "3D", "Room Premium 4D", "2026-06-25T16:00:00", 20.0),
        ("Interstellar", "2D_SUB", "Room Premium 4D", "2026-06-26T14:00:00", 20.0),
    ]

    with Session(engine) as session:
        function_service = FunctionService(session)

        for movie_title, movie_format, room_name, start_time, price in functions_to_seed:
            # Resolve Movie ID
            movie_stmt = select(Movie).where(Movie.title == movie_title, Movie.format == movie_format)
            movie = session.exec(movie_stmt).first()
            if not movie:
                print(f"###### Error: Movie '{movie_title}' ({movie_format}) not found. Skipping function.")
                continue

            # Resolve Room ID
            room_stmt = select(Room).where(Room.name == room_name)
            room = session.exec(room_stmt).first()
            if not room:
                print(f"###### Error: Room '{room_name}' not found. Skipping function.")
                continue

            # Check if this exact function already exists
            func_stmt = select(Function).where(
                Function.movie_id == movie.id,
                Function.room_id == room.id,
                Function.start_time == start_time
            )
            existing_function = session.exec(func_stmt).first()

            if not existing_function:
                function_create = FunctionCreate(
                    movie_id=movie.id,
                    room_id=room.id,
                    start_time=start_time,
                    price=price
                )
                try:
                    function_service.create(function_create)
                    print(f"-----> Creating function: Movie '{movie_title}' in Room '{room_name}' at {start_time}")
                except HTTPException as e:
                    print(f"###### Error creating function for '{movie_title}' in '{room_name}': {e.detail}")
            else:
                print(f"-----> Function for '{movie_title}' in '{room_name}' at {start_time} already exists. Skipping.")

        session.commit()
    print("Seed of Function completed successfully!")

if __name__ == "__main__":
    seed_function()