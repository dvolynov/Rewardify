# endpoints/api.py

from fastapi import APIRouter

from endpoints.auth           import router as auth_router
from endpoints.challenge      import router as challenge_router
from endpoints.user           import router as user_router
from endpoints.reward         import router as reward_router
from endpoints.challenge_log  import router as challenge_log_router
from endpoints.redemption     import router as redemption_router
from endpoints.wizard         import router as wizard_router
from endpoints.stat           import router as stat_router

router = APIRouter()

router.include_router(auth_router,          prefix="/auth")
router.include_router(challenge_router,     prefix="/challenge")
router.include_router(user_router,          prefix="/user")
router.include_router(reward_router,        prefix="/reward")
router.include_router(challenge_log_router, prefix="/challenge-log")
router.include_router(redemption_router,    prefix="/redemption")
router.include_router(wizard_router,        prefix="/wizard")
router.include_router(stat_router,          prefix="/stats")
