# database/crud/user.py

from .base import BaseDB


class UserDB(BaseDB):

    def __init__(self, db, User):
        super().__init__(db)
        self.User = User

    def get(self, email: str):
        return self._get_first(self.User, email=email)

    def add(self, name: str, email: str, password_hash: str, country: str):
        return self._add_if_not_exists(
            self.User,
            {"email": email},
            {
                "name": name,
                "email": email,
                "password_hash": password_hash,
                "country": country,
                "level": 1,
                "current_xp": 0,
                "points_total": 0
            }
        )

    def update(self, user_id: int, update_fields: dict):
        user = self._get_by_id(self.User, id=user_id)
        if not user:
            return None

        for field, value in update_fields.items():
            if value is not None:
                if field == "password":
                    setattr(user, "password_hash", value)
                elif hasattr(user, field):
                    setattr(user, field, value)

        return self._commit_refresh(user)