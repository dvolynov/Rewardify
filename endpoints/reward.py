# endpoints/reward.py

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse

import ai

from deps import db
from core.authentication import get_current_user
from core import exceptions
import schemas


router = APIRouter(tags=["Reward"])


@router.post("/generate", response_model=schemas.reward.RewardOut)
def generate_user_reward(data: schemas.reward.Prompt, user=Depends(get_current_user)):
    try:
        generated = ai.reward.generate(data.prompt)
    except Exception:
        raise exceptions.GENERATION_FAILED

    reward = db.reward.add(
        user_id     = user.id,
        name        = generated.name,
        description = generated.description,
        cost_points = generated.cost_points,
        icon        = generated.icon
    )

    return db.reward.get(reward.id, user.id)


@router.get("/", response_model=list[schemas.reward.RewardOut])
def get_user_rewards(user=Depends(get_current_user)):
    return db.reward.get_all(user.id)


@router.get("/{reward_hash}", response_model=schemas.reward.RewardOut)
def get_reward(reward_hash: str = Path(...), user=Depends(get_current_user)):
    reward = db.reward.get_by_hash(reward_hash, user.id)
    if not reward:
        raise exceptions.entity_not_found("Reward")
    return reward


@router.patch("/{reward_hash}/claim", response_model=schemas.reward.RewardOut)
def claim_reward(reward_hash: str = Path(...), user=Depends(get_current_user)):
    result = db.reward.claim(reward_hash, user)

    if result is None:
        raise exceptions.entity_not_found("Reward")
    if result == "already_claimed":
        raise exceptions.bad_request("Reward already claimed.")
    if result == "not_enough_points":
        raise exceptions.bad_request("Not enough points to claim this reward.")

    return result


@router.delete("/all", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_rewards(user=Depends(get_current_user)):
    success = db.reward.delete_all(user.id)
    if not success:
        raise exceptions.entity_not_found("Rewards")
    return JSONResponse(status_code=204, content=None)


@router.delete("/{reward_hash}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reward(reward_hash: str = Path(...), user=Depends(get_current_user)):
    success = db.reward.delete_by_hash(reward_hash, user.id)
    if not success:
        raise exceptions.entity_not_found("Reward")
    return JSONResponse(status_code=204, content=None)