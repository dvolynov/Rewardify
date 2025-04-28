# database/crud/reward.py

from datetime import datetime
from .base import BaseDB


class RewardDB(BaseDB):
    def __init__(self, db, Reward):
        super().__init__(db)
        self.Reward = Reward

    def get_all(self, user_id: int):
        rewards = self._get_all(self.Reward, user_id=user_id, order_by="created_at")
        rewards = sorted(rewards, key=lambda r: r.created_at, reverse=True)
        return [
            {column.name: getattr(r, column.name) for column in self.Reward.__table__.columns}
            for r in rewards
        ]

    def get(self, reward_id: int, user_id: int):
        return self._get_by_id(self.Reward, id=reward_id, user_id=user_id)

    def get_by_hash(self, reward_hash: str, user_id: int):
        return self._get_first(self.Reward, hash=reward_hash, user_id=user_id)

    def add(self, user_id: int, name: str, description: str, cost_points: int, icon: str, **kwargs):
        reward = self.Reward(
            user_id=user_id,
            name=name,
            description=description,
            cost_points=cost_points,
            icon=icon,
            **kwargs
        )
        self.db.add(reward)
        self.db.commit()
        self.db.refresh(reward)
        return reward

    def delete(self, reward_id: int, user_id: int) -> bool:
        return self._delete_by_filters(self.Reward, id=reward_id, user_id=user_id)

    def delete_by_hash(self, reward_hash: str, user_id: int) -> bool:
        reward = self.get_by_hash(reward_hash, user_id)
        if not reward:
            return False

        self.db.delete(reward)
        self.db.commit()
        return True

    def delete_all(self, user_id: int) -> bool:
        reward_ids = [r.id for r in self._get_all(self.Reward, user_id=user_id)]

        if not reward_ids:
            return False

        self.db.query(self.Reward).filter(self.Reward.user_id == user_id).delete(synchronize_session=False)
        self.db.commit()
        return True

    def claim(self, reward_hash: str, user):
        reward = self.get_by_hash(reward_hash, user.id)
        if not reward:
            return None

        if reward.claimed_at:
            return "already_claimed"

        if user.points_total < reward.cost_points:
            return "not_enough_points"

        user.points_total -= reward.cost_points
        reward.claimed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(reward)
        return reward