from sqlmodel import Session, select
from app.core.db import init_db, engine
from app.models.user import User, UserLogin, UserRole
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from fastapi import HTTPException

ADMIN_EMAILS = {"admin@email.com"}

def seed_user():
    init_db()

    # Initial data for users using UserLogin scheme
    users_data = [
        UserLogin(email="admin@email.com", password="123456"),
        UserLogin(email="user@email.com", password="123456"),
        UserLogin(email="juan@email.com", password="123456"),
        UserLogin(email="maria@email.com", password="123456"),
        UserLogin(email="carlos@email.com", password="123456"),
    ]

    print("Starting seed of users...")

    with Session(engine) as session:
        user_repo = UserRepository(session)
        auth_service = AuthService(user_repo)

        for u_data in users_data:
            # Check if user already exists
            statement = select(User).where(User.email == u_data.email)
            existing_user = session.exec(statement).first()

            if not existing_user:
                try:
                    existing_user = auth_service.register(u_data)
                    print(f"-----> Creating user: {u_data.email} with hashed password")
                except HTTPException as e:
                    print(f"###### Error creating user {u_data.email}: {e.detail}")
            else:
                print(f"-----> User {u_data.email} already exists. Skipping.")

            if existing_user and u_data.email in ADMIN_EMAILS and existing_user.role != UserRole.ADMIN:
                existing_user.role = UserRole.ADMIN
                session.add(existing_user)
                print(f"-----> Promoted {u_data.email} to admin")

        session.commit()

    print("Seed of User completed successfully!")

if __name__ == "__main__":
    seed_user()