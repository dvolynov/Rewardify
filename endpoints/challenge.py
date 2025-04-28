# endpoints/challenge.py

from fastapi import APIRouter, Depends, Path, Body, status
from fastapi.responses import JSONResponse

import ai

from deps import db
from core.authentication import get_current_user
from core import exceptions
import schemas


router = APIRouter(tags=["Challenge"])


@router.post("/generate", response_model=schemas.challenge.Out)
def generate_user_challenge(data: schemas.challenge.Prompt, user=Depends(get_current_user)):
    try:
        generated = ai.challenge.generate(data.prompt)
    except Exception:
        raise exceptions.GENERATION_FAILED

    challenge = db.challenge.add(
        user_id     = user.id,
        name        = generated.name,
        description = generated.description,
        icon        = generated.icon,
        goal_days   = generated.goal_days,
        difficulty  = generated.difficulty,
        time_of_day = generated.time_of_day,
        plan        = [step.dict() for step in generated.plan]
    )

    return db.challenge.get(challenge.id, user.id)


@router.get("/", response_model=list[schemas.challenge.Out])
def get_user_challenges(user=Depends(get_current_user)):
    return db.challenge.get_all(user.id)


@router.get("/{challenge_hash}", response_model=schemas.challenge.ChallengeDataOut)
def get_challenge(challenge_hash: str = Path(...), user=Depends(get_current_user)):
    challenge = db.challenge.get_with_plan_by_hash(challenge_hash, user.id)
    if not challenge:
        raise exceptions.entity_not_found("Challenge")
    return challenge


@router.patch("/{challenge_hash}/join", response_model=schemas.challenge.Out)
def join_challenge(challenge_hash: str = Path(...), user=Depends(get_current_user)):
    challenge = db.challenge.get_by_hash(challenge_hash, user.id)

    if not challenge:
        raise exceptions.entity_not_found("Challenge")

    updated = db.challenge.join(
        challenge_id=challenge.id,
        user_id=user.id
    )

    if not updated:
        raise exceptions.entity_not_found("Challenge")

    return db.challenge.get(challenge.id, user.id)


@router.patch("/{challenge_hash}/progress", response_model=schemas.challenge.Out)
def update_progress(challenge_hash: str = Path(...), user=Depends(get_current_user)):
    challenge = db.challenge.get_by_hash(challenge_hash, user.id)

    if not challenge:
        raise exceptions.entity_not_found("Challenge")

    updated = db.challenge.update_cur_day(
        challenge_id = challenge.id,
        user_id      = user.id,
        new_day      = challenge.cur_day + 1
    )
    if not updated:
        raise exceptions.entity_not_found("Challenge")

    return db.challenge.get(challenge.id, user.id)


@router.delete("/all", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_challenges(user=Depends(get_current_user)):
    success = db.challenge.delete_all(user_id=user.id)
    if not success:
        raise exceptions.entity_not_found("Challenges")
    return JSONResponse(status_code=204, content=None)


@router.delete("/{challenge_hash}", status_code=status.HTTP_204_NO_CONTENT)
def delete_challenge(challenge_hash: str = Path(...), user=Depends(get_current_user)):
    success = db.challenge.delete_by_hash(challenge_hash=challenge_hash, user_id=user.id)
    if not success:
        raise exceptions.entity_not_found("Challenge")
    return JSONResponse(status_code=204, content=None)