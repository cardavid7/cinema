# 🎬 Cinema Reservation API

A RESTful API for cinema seat reservation management built with **FastAPI**, **SQLModel**, and **PostgreSQL/SQLite**. Supports user authentication via JWT, transactional booking logic, and is ready for production deployment.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Database](#database)
- [Environment Variables](#environment-variables)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Overview

Cinema Reservation API provides a backend service for managing cinema reservations. It handles user registration, authentication, seat selection, and booking transactions with database-level integrity to prevent double bookings.

Key capabilities:

- User registration and login with JWT-based authentication
- Browse available movies and showtimes (functions)
- Manage rooms and seats
- Reserve seats with transactional safety (no double bookings)
- Token expiration management
- Error monitoring via Sentry integration
- Compatible with both **PostgreSQL** (production) and **SQLite** (development)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) `0.136.3` |
| ORM | [SQLModel](https://sqlmodel.tiangolo.com/) `0.0.38` + SQLAlchemy `2.0.50` |
| Database | PostgreSQL (via `psycopg` `3.3.4`) / SQLite (dev) |
| Validation | Pydantic `2.13.4` + pydantic-settings `2.14.1` |
| Auth | PyJWT `2.13.0` + pwdlib `0.3.0` (Argon2 hashing) |
| Server | Uvicorn `0.48.0` |
| Config | python-dotenv `1.2.2` |
| Monitoring | Sentry SDK `2.61.0` |
| CLI | FastAPI CLI `0.0.24` + Typer `0.26.3` |

---

## Project Structure

```
cinema/
├── app/
│   ├── main.py                      # FastAPI app entry point, router registration, lifespan
│   ├── api/
│   │   ├── depends.py               # Shared dependencies (DB session, current user)
│   │   └── routers/                 # API route handlers
│   │       ├── auth_router.py           # /auth  (register, login, token)
│   │       ├── movie_router.py          # /movies
│   │       ├── function_router.py       # /functions  (showtimes)
│   │       ├── room_router.py           # /rooms
│   │       ├── seat_router.py           # /seats
│   │       ├── reservation_router.py    # /reservations
│   │       └── user_router.py           # /users
│   ├── core/
│   │   ├── config.py                # Settings loaded from environment variables
│   │   ├── db.py                    # Database engine and session management
│   │   └── security.py              # JWT creation and password hashing utilities
│   ├── models/                      # SQLModel table definitions (ORM + schema)
│   │   ├── movie.py
│   │   ├── function.py
│   │   ├── room.py
│   │   ├── seat.py
│   │   ├── reservation.py
│   │   └── user.py
│   ├── repositories/                # Data access layer (database queries)
│   │   ├── movie_repository.py
│   │   ├── function_repository.py
│   │   ├── room_repository.py
│   │   ├── seat_repository.py
│   │   ├── reservation_repository.py
│   │   └── user_repository.py
│   ├── services/                    # Business logic and transactional operations
│   │   ├── auth_service.py
│   │   ├── movie_service.py
│   │   ├── function_service.py
│   │   ├── room_service.py
│   │   ├── seat_service.py
│   │   ├── reservation_service.py
│   │   └── user_service.py
│   └── seeds/                       # Seed scripts for initial data
│       └── run_all.py               # Runs every seeder in dependency order (idempotent)
├── frontend/                        # Angular SPA (see frontend/README.md)
├── render.yaml                      # Render Blueprint: DB + backend + frontend in one deploy
├── .env.example                     # Environment variable template
├── .gitignore
└── requirements.txt                 # Python dependencies
```

---

## Prerequisites

- **Python** 3.11 or higher
- **PostgreSQL** 14 or higher *(required for production; SQLite works for local development)*
- **pip** (Python package manager)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/cardavid7/cinema.git
cd cinema
```

### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

### 1. Set up environment variables

Copy the example file and fill in your values:

```bash
# Linux/macOS
cp .env.example .env

# Windows
copy .env.example .env
```

Then edit `.env` with your configuration (see [Environment Variables](#environment-variables) below).

### 2. Create the PostgreSQL database (production)

```sql
CREATE DATABASE cinema_db;
```

> For local development you can use a SQLite URL (e.g. `sqlite:///./cinema.db`) and skip this step.

The application uses SQLModel's `create_all()` on startup to auto-create all tables, so no manual migrations are needed for development.

---

## Running the Application

### Development mode (with hot reload)

```bash
fastapi dev app/main.py
```

or

```bash
uvicorn app.main:app --reload
```

### Production mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`.

---

## API Documentation

FastAPI automatically generates interactive documentation:

| Interface | URL |
|---|---|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |
| OpenAPI JSON | `http://localhost:8000/openapi.json` |

### Main Endpoints

All endpoints are prefixed with `/api/v1`.

#### 🔐 Auth

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | Register a new user | No |
| `POST` | `/api/v1/auth/login` | Login and receive a JWT token | No |
| `POST` | `/api/v1/auth/token` | OAuth2 password flow (for Swagger UI) | No |

#### 🎬 Movies

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/movies/{movie_id}` | Get a movie by ID | No |
| `GET` | `/api/v1/movies/title/{movie_title}` | Search movies by title | No |
| `POST` | `/api/v1/movies/` | Create a new movie | Yes |
| `PUT` | `/api/v1/movies/{movie_id}` | Update a movie | Yes |
| `DELETE` | `/api/v1/movies/{movie_id}` | Delete a movie | Yes |

#### 🕐 Functions (Showtimes)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/functions/` | List all functions | No |
| `GET` | `/api/v1/functions/{function_id}` | Get a function by ID | No |
| `POST` | `/api/v1/functions/` | Create a new function | Yes |
| `PUT` | `/api/v1/functions/{function_id}` | Update a function | Yes |
| `DELETE` | `/api/v1/functions/{function_id}` | Delete a function | Yes |

#### 🏛️ Rooms & Seats

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/rooms/` | List all rooms | No |
| `POST` | `/api/v1/rooms/` | Create a room | Yes |
| `GET` | `/api/v1/seats/` | List all seats | No |
| `POST` | `/api/v1/seats/` | Create a seat | Yes |

#### 🎟️ Reservations

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/reservations/{reservation_id}` | Get a reservation by ID | Yes |
| `GET` | `/api/v1/reservations/user/{user_id}` | List reservations by user | Yes |
| `GET` | `/api/v1/reservations/function/{function_id}` | List reservations by function | Yes |
| `POST` | `/api/v1/reservations/` | Create a reservation | Yes |
| `PUT` | `/api/v1/reservations/{reservation_id}` | Update a reservation | Yes |
| `DELETE` | `/api/v1/reservations/{reservation_id}` | Cancel a reservation | Yes |

> For the complete and interactive reference, visit `/docs` when the server is running.

---

## Authentication

The API uses **JWT (JSON Web Tokens)** for stateless authentication.

### Flow

1. Register a user via `POST /api/v1/auth/register`
2. Login via `POST /api/v1/auth/login` (pass `email` and `password` as query parameters) — you receive an `access_token`
3. Include the token in subsequent requests:

```http
Authorization: Bearer <your_access_token>
```

> **Tip:** In Swagger UI (`/docs`), use the `POST /api/v1/auth/token` endpoint (OAuth2 form) and then click the **Authorize** button to persist your token across all requests.

### Token configuration

Tokens expire based on `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` (default: `1440` minutes / 24 hours). Passwords are hashed using the **Argon2** algorithm via `pwdlib`.

---

## Database

The project uses **SQLModel** (built on top of SQLAlchemy) as the ORM and supports two backends:

| Environment | Backend | URL format |
|---|---|---|
| Development | SQLite | `sqlite:///./cinema.db` |
| Production | PostgreSQL | `postgresql+psycopg://user:password@host:5432/dbname` |

### Connection

The database backend is automatically detected from the `DATABASE_URL` environment variable. SQLite requires no additional installation; PostgreSQL requires `psycopg` (included in `requirements.txt`).

> **Note:** Managed providers (Render, Railway, Heroku, etc.) often hand out connection strings prefixed with `postgres://` or plain `postgresql://`. `app/core/db.py` normalizes both to `postgresql+psycopg://` automatically, so you can paste the provider's URL as-is into `DATABASE_URL`.

### Seeding data

`app/seeds/` contains one script per entity plus `run_all.py`, which runs them in the required dependency order (`user → movie → room → seat → function → reservation`). Every seeder checks for existing rows before inserting, so it's safe to re-run — including on every application startup in production (see [Deployment](#deployment)).

```bash
python -m app.seeds.run_all
```

### Transactions

Reservation creation uses database transactions to guarantee atomicity, preventing race conditions such as double-booking of the same seat.

---

## Environment Variables

All configuration is managed through environment variables. Copy `.env.example` to `.env` and fill in the values:

```env
# Database connection string
# SQLite (development):
DATABASE_URL=sqlite:///./cinema.db
# PostgreSQL (production):
# DATABASE_URL=postgresql+psycopg://user:password@host:5432/dbname

# JWT configuration
JWT_SECRET_KEY=your-super-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

| Variable | Description | Required |
|---|---|---|
| `DATABASE_URL` | Full database connection URI (SQLite or PostgreSQL) | ✅ |
| `JWT_SECRET_KEY` | Secret key used to sign JWT tokens | ✅ |
| `JWT_ALGORITHM` | Algorithm for JWT signing (e.g. `HS256`) | ✅ |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes | ✅ |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins (e.g. `https://cinema-frontend.onrender.com,http://localhost:4200`) | ✅ |

> **Security note:** Never commit your `.env` file to version control. It is already included in `.gitignore`.

---

## Deployment

This repository is set up to deploy as **three independent services**: a PostgreSQL database, this FastAPI backend, and the [Angular frontend](frontend/README.md#deployment). It also serves a single-process mode where the backend serves the built Angular app for every non-API route — useful for smaller or all-in-one deployments — but the split setup below is recommended for Render's free tier, since static sites don't sleep while free web services do.

### Deploying to Render

1. **Database** — create a **PostgreSQL** instance (Free plan). Copy its *Internal Database URL*.
2. **Backend** — create a **Web Service** from this repo:
   - Build command: `pip install -r requirements.txt`
   - Start command:
     ```bash
     python -m app.seeds.run_all && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
     Running the seeders before `uvicorn` on every boot is safe because they're idempotent — this keeps the catalog populated without a separate release step.
   - Environment variables: `DATABASE_URL` (from step 1), `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`, and `CORS_ORIGINS` (set once the frontend URL is known — step 3).
3. **Frontend** — deploy as a **Static Site** as described in [frontend/README.md](frontend/README.md#deployment), pointing its `API_URL` build variable at this service's URL.
4. Update `CORS_ORIGINS` on the backend with the frontend's final URL and redeploy.

A ready-to-use [`render.yaml`](render.yaml) Blueprint is included to provision all three resources in one step (**New +** → **Blueprint** in the Render dashboard). Because the frontend and backend URLs reference each other, double-check `CORS_ORIGINS` and `API_URL` after the first deploy in case Render assigned different hostnames than the ones predicted in the file.

---

## Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## License

This project is open source. See the repository for details.

---

> Built with ❤️ using [FastAPI](https://fastapi.tiangolo.com/)