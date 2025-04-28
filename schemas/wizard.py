# schemas/wizard.py

from pydantic import BaseModel
from typing import List, Optional


class WizardRequest(BaseModel):
    goal: str
    current_level: Optional[str]
    available_time: Optional[int]
    interests: Optional[List[str]]

class WizardResponse(BaseModel):
    suggested_challenges: List[str]
    suggested_rewards: List[str]