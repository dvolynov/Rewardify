# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints import router
from tools import print_settings
import settings


app = FastAPI(
    title       = settings.general.APP_NAME,
    description = "Turn good habits into real points, track your daily challenges, and redeem rewards. Designed for progressive behavior change through AI-assisted goal setting and personalized challenge building.",
    version     = "1.0.0",
    debug       = settings.general.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials = True,
    allow_origins     = ["*"],
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

app.include_router(router, prefix="/api")


if settings.general.DEBUG:
    print(f"[DEBUG] Starting in {settings.general.ENVIRONMENT} mode with debug enabled.")
    print_settings()