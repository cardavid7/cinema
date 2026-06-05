from app.core.db import init_db, engine
from sqlmodel import Session, select
from app.models.function import Function
from datetime import datetime, timedelta
from enum import Enum


def seed_function():
    # Starting database table creation
    init_db()

    # Initial data for functions
    functions_data = [
        {"movie_id": 1, "room_id": 1, "start_time": "2022-01-01T12:00:00", "end_time": "2022-01-01T14:00:00", "price": 10.0},
        {"movie_id": 1, "room_id": 1, "start_time": "2022-01-01T15:00:00", "end_time": "2022-01-01T17:00:00", "price": 12.0},
        {"movie_id": 1, "room_id": 2, "start_time": "2022-01-01T18:00:00", "end_time": "2022-01-01T20:00:00", "price": 14.0},
        {"movie_id": 1, "room_id": 3, "start_time": "2022-01-01T21:00:00", "end_time": "2022-01-01T23:00:00", "price": 16.0},
    ]

    print("Starting seed of functions...")

    with Session(engine) as session:
        for f_data in functions_data:
            statement = select(Function).where(Function.movie_id == f_data["movie_id"]).where(Function.room_id == f_data["room_id"]).where(Function.start_time == f_data["start_time"])
            existing_function = session.exec(statement).first()
            if not existing_function:
                function = Function(movie_id=f_data["movie_id"], room_id=f_data["room_id"], start_time=f_data["start_time"], end_time=f_data["end_time"], price=f_data["price"])
                session.add(function)
                print(f"-----> Creating function: {f_data['movie_id']} - {f_data['room_id']} - {f_data['start_time']} - {f_data['end_time']} - {f_data['price']}")
            else:
                print(f"-----> Function {f_data['movie_id']} - {f_data['room_id']} - {f_data['start_time']} - {f_data['end_time']} - {f_data['price']} already exists. Skipping.")

        session.commit()
    print("Seed of Function completed successfully!")

if __name__ == "__main__":
    seed_function()