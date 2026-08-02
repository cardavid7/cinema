from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist" / "frontend" / "browser"

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

if FRONTEND_DIST.is_dir():
    # Production: serve the built Angular app for every non-API path so a
    # single process handles both the API and the SPA (client-side routing
    # falls back to index.html for deep links like /movies/5).
    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        candidate = FRONTEND_DIST / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")
else:
    # Development: frontend/dist doesn't exist because the Angular app runs
    # separately via `ng serve` (see frontend/README or proxy.conf.json).
    @app.get("/")
    def read_root():
        return {
            "message": "Welcome to Cinema API",
            "docs": "/docs",
            "status": "online"
        }
