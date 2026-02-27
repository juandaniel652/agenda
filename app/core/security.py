from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY no configurada")

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
