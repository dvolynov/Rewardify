# schemas/stat.py

from pydantic import BaseModel
from typing import Optional


class StatResponse(BaseModel):
    total_points: int
    completed_challenges: int
    redeemed_rewards: int
    current_streak: Optional[int]
    total_days_logged: int


class LevelStatResponse(BaseModel):
    level: int
    current_xp: int
    xp_for_next_level: int
    points_total: int