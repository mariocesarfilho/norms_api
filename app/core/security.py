from datetime import datetime, timedelta, timezone
import jwt

from app.core.config import settings

def encode(subject:str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire
    )

    payload = {
        "sub": subject,
        "exp": expires_at
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings
    )

def decode(token: str) -> str:
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )