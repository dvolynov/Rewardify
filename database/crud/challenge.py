# database/crud/challenge.py

from sqlalchemy import func
from .base import BaseDB


class ChallengeDB(BaseDB):
    def __init__(self, db, Challenge, Milestone):
        super().__init__(db)
        self.Challenge = Challenge
        self.Milestone = Milestone

    def get_all(self, user_id: int):
        challenges = self._get_all(self.Challenge, user_id=user_id, order_by="created_at")
        challenges = sorted(challenges, key=lambda ch: ch.created_at, reverse=True)
        return [
            {column.name: getattr(ch, column.name) for column in self.Challenge.__table__.columns}
            for ch in challenges
        ]

    def get(self, challenge_id: int, user_id: int):
        return self._get_by_id(self.Challenge, id=challenge_id, user_id=user_id)

    def get_by_hash(self, challenge_hash: str, user_id: int):
        return self._get_first(self.Challenge, hash=challenge_hash, user_id=user_id)

    def add(self, user_id: int, name: str, description: str, icon: str, goal_days: int, difficulty: str, time_of_day: str, plan: list[dict], **kwargs):
        challenge = self.Challenge(
            user_id     = user_id,
            name        = name,
            description = description,
            goal_days   = goal_days,
            difficulty  = difficulty,
            time_of_day = time_of_day,
            icon        = icon,
            **kwargs
        )
        self.db.add(challenge)
        self.db.flush()

        milestones = [
            self.Milestone(
                challenge_id=challenge.id,
                day=step["day"],
                title=step["title"],
                description=step["description"],
                icon=step["icon"]
            )
            for step in plan
        ]
        self.db.bulk_save_objects(milestones)
        self.db.commit()
        self.db.refresh(challenge)
        return challenge

    def delete(self, challenge_id: int, user_id: int) -> bool:
        return self._delete_by_filters(self.Challenge, id=challenge_id, user_id=user_id)

    def delete_by_hash(self, challenge_hash: str, user_id: int) -> bool:
        challenge = self.get_by_hash(challenge_hash, user_id)
        if not challenge:
            return False

        milestones = self._get_all(self.Milestone, challenge_id=challenge.id)
        for milestone in milestones:
            self.db.delete(milestone)

        self.db.delete(challenge)
        self.db.commit()
        return True

    def update_cur_day(self, challenge_id: int, user_id: int, new_day: int):
        return self._update_or_create(
            self.Challenge,
            filters={"id": challenge_id, "user_id": user_id},
            update_data={"cur_day": new_day}
        )

    def get_with_plan(self, challenge_id: int, user_id: int):
        challenge = self.get(challenge_id, user_id)
        if not challenge:
            return None

        milestones = self._get_all(self.Milestone, challenge_id=challenge.id)
        milestones_sorted = sorted(milestones, key=lambda m: m.day)

        challenge_data = {column.name: getattr(challenge, column.name) for column in self.Challenge.__table__.columns}
        challenge_data["plan"] = [
            {column.name: getattr(m, column.name) for column in self.Milestone.__table__.columns}
            for m in milestones_sorted
        ]
        return challenge_data

    def get_with_plan_by_hash(self, challenge_hash: str, user_id: int):
        challenge = self.get_by_hash(challenge_hash, user_id)
        if not challenge:
            return None

        milestones = self._get_all(self.Milestone, challenge_id=challenge.id)
        milestones_sorted = sorted(milestones, key=lambda m: m.day)

        challenge_data = {column.name: getattr(challenge, column.name) for column in self.Challenge.__table__.columns}
        challenge_data["plan"] = [
            {column.name: getattr(m, column.name) for column in self.Milestone.__table__.columns}
            for m in milestones_sorted
        ]
        return challenge_data

    def delete_all(self, user_id: int) -> bool:
        challenge_ids = [c.id for c in self._get_all(self.Challenge, user_id=user_id)]

        if not challenge_ids:
            return False

        self.db.query(self.Milestone).filter(self.Milestone.challenge_id.in_(challenge_ids)).delete(synchronize_session=False)
        self.db.query(self.Challenge).filter(self.Challenge.user_id == user_id).delete(synchronize_session=False)
        self.db.commit()
        return True

    def join(self, challenge_id: int, user_id: int):
        return self._update_or_create(
            self.Challenge,
            filters={"id": challenge_id, "user_id": user_id},
            update_data={"cur_day": 0, "joined_at": func.now()}
        )