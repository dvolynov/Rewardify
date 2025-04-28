# core/authentification.py

from fastapi import Depends
from datetime import datetime, timedelta, timezone
from typing import Optional
from jwt import PyJWTError
import jwt

from deps import db, pwd_context, oauth2_scheme
from core import exceptions as exc
import settings


# Hash and verify password
verify_password = lambda plain, hashed: pwd_context.verify(plain, hashed)
hash_password = lambda password: pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Generate JWT access token with optional expiration"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.auth.EXPIRES_DAYS * 24 * 60)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.auth.SECRET_KEY,
        algorithm=settings.auth.ALGORITHM
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from access token"""
    try:
        payload = jwt.decode(
            token,
            settings.auth.SECRET_KEY,
            algorithms=[settings.auth.ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise exc.UNAUTHORIZED
    except PyJWTError:
        raise exc.UNAUTHORIZED

    user = db.user.get(email=email)
    if user is None:
        raise exc.UNAUTHORIZED

    return user