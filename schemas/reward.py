# schemas/reward.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RewardCreate(BaseModel):
    name: str
    description: str
    cost_points: int
    icon: str


class RewardOut(BaseModel):
    id: int
    name: str
    description: str
    cost_points: int
    icon: str
    hash: str
    created_at: datetime
    claimed_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Prompt(BaseModel):
    prompt: str