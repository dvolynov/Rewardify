# database/models/reward_redemption.py

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from .base import Base


class RewardRedemption(Base):
    __tablename__ = "reward_redemptions"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reward_id   = Column(Integer, ForeignKey("rewards.id", ondelete="CASCADE"), nullable=False)
    redeemed_at = Column(TIMESTAMP, server_default=func.now())