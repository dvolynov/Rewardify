# database/models/challenge.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base
import hashlib
import time


def generate_challenge_hash():
    raw = f"{time.time_ns()}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


class Challenge(Base):
    __tablename__ = "challenges"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    user_id      = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name         = Column(String, nullable=False)
    description  = Column(Text, nullable=False)
    cur_day      = Column(Integer, default=0)
    goal_days    = Column(Integer, nullable=False)
    difficulty   = Column(String(10), nullable=False)
    time_of_day  = Column(String(10), nullable=False)
    icon         = Column(Text, nullable=False)
    created_at   = Column(TIMESTAMP, server_default=func.now())
    joined_at    = Column(TIMESTAMP, nullable=True)
    finished_at  = Column(TIMESTAMP, nullable=True)
    hash         = Column(String(64), nullable=False, unique=True, default=generate_challenge_hash)

    user         = relationship("User", back_populates="challenges")

    __table_args__ = (
        UniqueConstraint('hash', name='uq_challenge_hash'),
    )