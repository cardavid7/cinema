from app.core.db import init_db, engine
from sqlmodel import Session, select
from app.models.user import User


def seed_user():
    # Starting database tables creation
    init_db()

    # Initial data for users
    users_data = [
        {"username": "Admin", "email": "admin@email.com", "hashed_password": "123456", "is_active": True},
        {"username": "User", "email": "user@email.com", "hashed_password": "123456", "is_active": True},
    ]

    print("Starting seed of users...")

    with Session(engine) as session:
        for u_data in users_data:
            statement = select(User).where(User.email == u_data["email"])
            existing_user = session.exec(statement).first()

            if not existing_user:
                user = User(username=u_data["username"], email=u_data["email"], hashed_password=u_data["hashed_password"], is_active=u_data["is_active"])
                session.add(user)
                print(f"-----> Creating user: {u_data['email']} - {u_data['username']}")
            else:
                print(f"-----> User {u_data['email']} - {u_data['username']} already exists. Skipping.")

        session.commit()

    print("Seed of User completed successfully!")

if __name__ == "__main__":
    seed_user()