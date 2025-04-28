# ai/challenge.py

from openai import OpenAI
from pydantic import BaseModel
from typing import List, Literal

import settings


client = OpenAI(api_key=settings.ai.API_KEY)

with open("./ai/instructions/challenge.txt", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


class Milestone(BaseModel):
    day: int
    title: str
    description: str
    icon: str


class Challenge(BaseModel):
    name: str
    description: str
    icon: str
    goal_days: int
    difficulty: Literal["easy", "medium", "hard"]
    time_of_day: Literal["morning", "afternoon", "evening"]
    plan: List[Milestone]


def generate(prompt: str):

    response = client.responses.parse(
        model = settings.ai.MODEL,
        input = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        text_format = Challenge
    )

    parsed = response.output_parsed

    return Challenge(
        name         = parsed.name,
        description  = parsed.description,
        icon         = parsed.icon,
        goal_days    = parsed.goal_days,
        difficulty   = parsed.difficulty,
        time_of_day  = parsed.time_of_day,
        plan         = [
            Milestone(
                day         = step.day,
                title       = step.title,
                description = step.description,
                icon        = step.icon
            ) for step in parsed.plan
        ]
    )