from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import init_db
from app.seeds.room import seed_rooms

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application and database...")
    try:
        init_db()
        print("Database initialized (tables created).")

    except Exception as e:
        print(f"###### ERROR: {e}")
    
    yield
    print("Shutting down the application...")

app = FastAPI(
    title="Cinema API",
    description="API for the management of rooms, movies, functions, seats and reservations of cinema.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Cinema API",
        "docs": "/docs",
        "status": "online"
    }
