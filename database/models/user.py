# database/models/user.py

from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "users"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    name           = Column(String, nullable=False)
    country        = Column(String, nullable=False)
    email          = Column(String, unique=True, nullable=False)
    password_hash  = Column(String, nullable=False)
    level          = Column(Integer, default=1)
    current_xp     = Column(Integer, default=0)
    points_total   = Column(Integer, default=0)
    created_at     = Column(TIMESTAMP, server_default=func.now())

    challenges     = relationship("Challenge", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"