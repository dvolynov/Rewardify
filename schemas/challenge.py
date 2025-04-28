# schemas/challenge.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Milestone(BaseModel):
    id: int
    day: int
    title: str
    description: str
    icon: str
    points: Optional[int] = None

    class Config:
        orm_mode = True


class Out(BaseModel):
    id: int
    name: str
    description: str
    cur_day: int
    goal_days: int
    created_at: datetime
    icon: str
    hash: str
    joined_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Prompt(BaseModel):
    prompt: str


class ChallengeDataOut(BaseModel):
    id: int
    name: str
    description: str
    cur_day: int
    goal_days: int
    created_at: datetime
    icon: str
    hash: str
    joined_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    plan: List[Milestone]

    class Config:
        orm_mode = True