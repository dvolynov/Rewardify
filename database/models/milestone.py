# database/models/milestone.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Milestone(Base):
    __tablename__ = "milestones"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False)
    day          = Column(Integer, nullable=False)
    title        = Column(String, nullable=False)
    description  = Column(Text, nullable=False)
    icon         = Column(Text, nullable=False)

    challenge    = relationship("Challenge", backref="milestones")