# deps.py

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from database import Database


# Init Database Session
db             = Database()
pwd_context    = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="api/auth/token")