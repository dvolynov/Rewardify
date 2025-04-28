# core/exceptions.py

from fastapi import HTTPException, status


USER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

USER_CREATION_FAILED = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="User could not be created"
)

EMAIL_ALREADY_REGISTERED = HTTPException(
    status_code=400,
    detail="Email is already registered."
)

UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email or password"
)

GENERATION_FAILED = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Generation failed. Please try again later."
)

REWARD_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Reward not found."
)

REDEMPTION_FAILED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to redeem reward."
)

CHALLENGE_LOG_CREATION_FAILED = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failed to log challenge progress."
)


def entity_not_found(entity: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} not found"
    )

def creation_failed(entity: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"{entity} could not be created"
    )

def bad_request(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )