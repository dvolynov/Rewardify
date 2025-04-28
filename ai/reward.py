# ai/reward.py

from openai import OpenAI
from pydantic import BaseModel

import settings


client = OpenAI(api_key=settings.ai.API_KEY)

with open("./ai/instructions/reward.txt", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


class Reward(BaseModel):
    name: str
    description: str
    icon: str
    cost_points: int


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
        text_format = Reward
    )

    parsed = response.output_parsed

    return Reward(
        name         = parsed.name,
        description  = parsed.description,
        icon         = parsed.icon,
        cost_points  = parsed.cost_points
    )