# schemas/redemption.py

from pydantic import BaseModel
from datetime import datetime


class RedemptionCreate(BaseModel):
    reward_id: int
    spent_points: int


class RedemptionOut(BaseModel):
    id: int
    reward_id: int
    spent_points: int
    redeemed_at: datetime

    class Config:
        orm_mode = True