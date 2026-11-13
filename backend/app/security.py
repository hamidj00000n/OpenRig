from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.config import ACCESS_TOKEN_MINUTES, SECRET_KEY

ALGORITHM = "HS256"
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def create_access_token(user_id: str) -> tuple[str, int]:
    expires = ACCESS_TOKEN_MINUTES * 60
    now = datetime.now(timezone.utc)
    payload = {"sub": user_id, "iat": now, "exp": now + timedelta(seconds=expires)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM), expires


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject = payload.get("sub")
        return subject if isinstance(subject, str) else None
    except JWTError:
        return None
