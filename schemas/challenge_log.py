# schemas/challenge_log.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChallengeLogCreate(BaseModel):
    challenge_id: int
    milestone_id: Optional[int] = None
    base_points: int


class ChallengeLogOut(BaseModel):
    id: int
    challenge_id: int
    milestone_id: Optional[int] = None
    base_points: int
    bonus_points: int
    total_points: int
    logged_at: datetime

    class Config:
        orm_mode = True