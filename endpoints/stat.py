# endpoints/stat.py

from fastapi import APIRouter, Depends

from core.authentication import get_current_user
import schemas
from deps import db


router = APIRouter(tags=["Stats"])


@router.get("/", response_model=schemas.stat.StatResponse)
def get_user_stats(user=Depends(get_current_user)):
    return schemas.stat.StatResponse(
        total_points         = db.challenge_log.get_total_points(user_id=user.id),
        completed_challenges = db.challenge_log.get_completed_challenges_count(user_id=user.id),
        redeemed_rewards     = db.reward_redemption.get_redeemed_rewards_count(user_id=user.id),
        current_streak       = db.challenge_log.get_current_streak(user_id=user.id),
        total_days_logged    = db.challenge_log.get_total_days_logged(user_id=user.id)
    )


@router.get("/level", response_model=schemas.stat.LevelStatResponse)
def get_user_level_info(user=Depends(get_current_user)):
    return schemas.stat.LevelStatResponse(
        level             = user.level,
        current_xp        = user.current_xp,
        xp_for_next_level = user.level * 100,
        points_total      = user.points_total
    )