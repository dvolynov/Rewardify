# endpoints/redemption.py

from fastapi import APIRouter, Depends, status
from deps import db
from core.authentication import get_current_user
import schemas

router = APIRouter(tags=["Redemptions"])


@router.post("/", response_model=schemas.redemption.RedemptionOut, status_code=status.HTTP_201_CREATED)
def redeem_reward(payload: schemas.redemption.RedemptionCreate, user=Depends(get_current_user)):
    redemption = db.redemption.add(
        user_id=user.id,
        reward_id=payload.reward_id,
        spent_points=payload.spent_points
    )
    return redemption


@router.get("/", response_model=list[schemas.redemption.RedemptionOut])
def get_redemptions(user=Depends(get_current_user)):
    return db.redemption.get_all(user.id)