# endpoints/user.py

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from deps import db
from core.authentication import get_current_user, hash_password, verify_password
from core import exceptions
import schemas


router = APIRouter(tags=["User"])

@router.get("/", response_model=schemas.user.Out)
def get_user(user=Depends(get_current_user)):
    return db.user.get(user.email)



@router.patch("/update", response_model=schemas.user.Out)
def update_user(data: schemas.user.Update, user=Depends(get_current_user)):
    update_fields = data.dict(exclude_unset=True)

    if "old_password" in update_fields or "new_password" in update_fields:
        old_password = update_fields.pop("old_password", None)
        new_password = update_fields.pop("new_password", None)

        if not old_password or not new_password:
            raise exceptions.bad_request("Both old_password and new_password must be provided.")

        if not verify_password(old_password, user.password_hash):
            raise exceptions.bad_request("Incorrect current password.")

        update_fields["password"] = hash_password(new_password)

    updated_user = db.user.update(user.id, update_fields)
    return updated_user


@router.delete("/delete")
def delete_user(user=Depends(get_current_user)):
    success = db.delete_user(user_id=user.id)
    if not success:
        raise exceptions.entity_not_found("user")
    return JSONResponse(status_code=204, content=None)