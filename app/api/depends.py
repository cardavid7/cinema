from typing import Iterator, Annotated
from fastapi import Depends
from sqlmodel import Session

from app.core.db import get_session

def get_db() -> Iterator[Session]:
    yield from get_session()

DBSession = Annotated[Session, Depends(get_db)]