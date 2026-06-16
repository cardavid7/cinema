from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import init_db
from app.api.routers.room_router import router as room_router
from app.api.routers.seat_router import router as seat_router
from app.api.routers.movie_router import router as movie_router
from app.api.routers.function_router import router as function_router

API_PREFIX = "/api/v1"

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

app.include_router(room_router, prefix=API_PREFIX)
app.include_router(seat_router, prefix=API_PREFIX)
app.include_router(movie_router, prefix=API_PREFIX)
app.include_router(function_router, prefix=API_PREFIX)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Cinema API",
        "docs": "/docs",
        "status": "online"
    }
