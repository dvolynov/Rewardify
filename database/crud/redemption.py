# database/crud/redemption.py

from .base import BaseDB


class RedemptionDB(BaseDB):
    def __init__(self, db, Redemption):
        super().__init__(db)
        self.Redemption = Redemption

    def get_all(self, user_id: int):
        return self._get_all(self.Redemption, user_id=user_id)

    def add(self, user_id: int, reward_id: int, spent_points: int):
        return self._create(
            self.Redemption,
            user_id=user_id,
            reward_id=reward_id,
            spent_points=spent_points
        )