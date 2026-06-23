from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt

from app.core.config import settings

password_hash = PasswordHash.recommended()

def hash_password(plain_password: str) -> str:
    return password_hash.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise Exception(f"Expired authentication token: {e}")
    except jwt.InvalidTokenError as e:
        raise Exception(f"Invalid authentication credentials (InvalidTokenError): {e}")
    except Exception as e:
        raise Exception(f"Invalid authentication credentials (other Exception): {e}")
        