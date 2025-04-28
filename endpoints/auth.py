# endpoints/auth.py

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.authentication import create_access_token, verify_password, hash_password
from core import exceptions
import schemas
from deps import db


router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=schemas.auth.TokenResponse)
def register_user(payload: schemas.auth.RegisterRequest):
    """Registers a new user if the email is not already taken."""
    existing_user = db.user.get(payload.email)
    if existing_user:
        raise exceptions.EMAIL_ALREADY_REGISTERED

    user = db.user.add(
        name          = payload.name,
        email         = payload.email,
        password_hash = hash_password(payload.password),
        country       = payload.country
    )
    user = authenticate_user(payload.email, payload.password, db)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token}


def authenticate_user(email: str, password: str, db):
    user = db.user.get(email)
    if not user or not verify_password(password, user.password_hash):
        raise exceptions.UNAUTHORIZED
    return user


@router.post("/token", response_model=schemas.auth.TokenResponse)
def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2-compatible token endpoint for form-based login."""
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token}


@router.post("/login", response_model=schemas.auth.TokenResponse)
def login_user(payload: schemas.auth.LoginRequest):
    """Authenticates user credentials and returns an access token."""
    user = authenticate_user(payload.email, payload.password, db)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token}