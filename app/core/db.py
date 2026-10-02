from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# Import models to ensure they are registered in SQLModel.metadata

def _normalize_database_url(url: str) -> str:
    # Neon (and other providers) hand out "postgres://" or plain
    # "postgresql://" URLs, but SQLAlchemy needs the psycopg driver spelled
    # out explicitly since psycopg2 isn't installed in this project.
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

DATABASE_URL = _normalize_database_url(settings.DATABASE_URL)
IS_SQLITE = "sqlite" in DATABASE_URL

connect_args = {"check_same_thread": False} if IS_SQLITE else {}
engine_kwargs = {}

if not IS_SQLITE:
    # Neon only accepts TLS connections; enforce it even if the URL omits it.
    if "neon.tech" in DATABASE_URL and "sslmode=" not in DATABASE_URL:
        connect_args["sslmode"] = "require"
    # Neon suspends idle computes and drops their connections, so validate
    # pooled connections before use and recycle them before they go stale.
    engine_kwargs = {"pool_pre_ping": True, "pool_recycle": 300}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args, **engine_kwargs)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
