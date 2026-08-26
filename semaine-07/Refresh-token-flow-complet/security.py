from datetime import UTC, datetime, timedelta
from uuid import uuid4
from jose import JWTError, jwt

SECRET_KEY = "super-secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(user_id: str) -> str:
    """Crée un access token JWT."""
    now = datetime.now(UTC)
    payload = {
        "sub": user_id,
        "type": "access",
        "jti": str(uuid4()),
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Crée un refresh token JWT."""
    now = datetime.now(UTC)
    payload = {
        "sub": user_id,
        "type": "refresh",
        "jti": str(uuid4()),
        "iat": now,
        "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, object]:
    """Vérifie la signature et l'expiration du token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as exc:
        raise ValueError("Token invalide ou expiré") from exc
