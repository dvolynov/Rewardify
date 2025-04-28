# database/models/challenge_log.py

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func
from .base import Base


class ChallengeLog(Base):
    __tablename__ = "challenge_logs"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    user_id       = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    challenge_id  = Column(Integer, ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    milestone_id  = Column(Integer, ForeignKey("milestones.id", ondelete="CASCADE"), nullable=True)
    earned_points = Column(Integer, nullable=False)
    logged_at     = Column(TIMESTAMP, server_default=func.now())