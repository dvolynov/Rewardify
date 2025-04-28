# database/models/reward.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base
import hashlib
import time


def generate_reward_hash():
    raw = f"{time.time_ns()}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


class Reward(Base):
    __tablename__ = "rewards"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name        = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    cost_points = Column(Integer, nullable=False)
    icon        = Column(Text, nullable=False)
    created_at  = Column(TIMESTAMP, server_default=func.now())
    claimed_at  = Column(TIMESTAMP, nullable=True)
    hash        = Column(String(64), nullable=False, unique=True, default=generate_reward_hash)

    user        = relationship("User", backref="rewards")

    __table_args__ = (
        UniqueConstraint('hash', name='uq_reward_hash'),
    )