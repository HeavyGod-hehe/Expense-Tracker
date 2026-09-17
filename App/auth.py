from pwdlib import PasswordHash
from pydantic_settings import BaseSettings, SettingsConfigDict
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    JWT_SECRET_KEY: str


settings = Settings()

ALGORITHM = "HS256"


def create_access_token(data):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    result = password_hash.verify(
        plain_password,
        hashed_password
    )

    return result


def verify_access_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )