# endpoints/challenge_log.py

from fastapi import APIRouter, Depends, status
from deps import db
from core.authentication import get_current_user
import schemas

router = APIRouter(tags=["Challenge Log"])


@router.post("/", response_model=schemas.challenge_log.ChallengeLogOut, status_code=status.HTTP_201_CREATED)
def log_challenge(payload: schemas.challenge_log.ChallengeLogCreate, user=Depends(get_current_user)):
    challenge_log = db.challenge_log.add(
        user_id      = user.id,
        challenge_id = payload.challenge_id,
        milestone_id = payload.milestone_id,
        base_points  = payload.earned_points
    )
    return challenge_log


@router.get("/", response_model=list[schemas.challenge_log.ChallengeLogOut])
def get_challenge_logs(user=Depends(get_current_user)):
    return db.challenge_log.get_all(user.id)