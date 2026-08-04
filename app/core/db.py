from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# Import models to ensure they are registered in SQLModel.metadata

def _normalize_database_url(url: str) -> str:
    # Render (and other providers) hand out "postgres://" or plain
    # "postgresql://" URLs, but SQLAlchemy needs the psycopg driver spelled
    # out explicitly since psycopg2 isn't installed in this project.
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

DATABASE_URL = _normalize_database_url(settings.DATABASE_URL)
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
