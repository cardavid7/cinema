from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from app.core.db import init_db
from app.api.routers.room_router import router as room_router
from app.api.routers.seat_router import router as seat_router
from app.api.routers.movie_router import router as movie_router
from app.api.routers.function_router import router as function_router
from app.api.routers.user_router import router as user_router
from app.api.routers.reservation_router import router as reservation_router
from app.api.routers.auth_router import router as auth_router

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
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(reservation_router, prefix=API_PREFIX)
app.include_router(function_router, prefix=API_PREFIX)
app.include_router(movie_router, prefix=API_PREFIX)
app.include_router(room_router, prefix=API_PREFIX)
app.include_router(seat_router, prefix=API_PREFIX)
app.include_router(user_router, prefix=API_PREFIX)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Cinema API",
        "docs": "/docs",
        "status": "online"
    }
