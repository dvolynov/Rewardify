# endpoints/wizard.py

from fastapi import APIRouter, Depends

from core.authentication import get_current_user
import schemas


router = APIRouter(tags=["Wizard"])


@router.post("/setup", response_model=schemas.wizard.WizardResponse)
def setup_wizard(data: schemas.wizard.WizardRequest, user=Depends(get_current_user)):
    suggested_challenges = [...]
    suggested_rewards = [...]
    return schemas.wizard.WizardResponse(
        suggested_challenges=suggested_challenges,
        suggested_rewards=suggested_rewards
    )