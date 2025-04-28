# database/crud/challenge_log.py

from .base import BaseDB
from tools import bonus
from datetime import datetime, timedelta


class ChallengeLogDB(BaseDB):
    def __init__(self, db, ChallengeLog):
        super().__init__(db)
        self.ChallengeLog = ChallengeLog

    def get_all(self, user_id: int):
        return self._get_all(self.ChallengeLog, user_id=user_id)

    def add(self, user_id: int, challenge_id: int, milestone_id: int | None, base_points: int):
        bonus = self.calculate_user_bonus(user_id)
        total_points = base_points + bonus

        return self._create(
            self.ChallengeLog,
            user_id       = user_id,
            challenge_id  = challenge_id,
            milestone_id  = milestone_id,
            earned_points = total_points
        )

    def get_last_log_date(self, user_id: int):
        last_log = (
            self.db.query(self.ChallengeLog)
            .filter_by(user_id=user_id)
            .order_by(self.ChallengeLog.logged_at.desc())
            .first()
        )
        return last_log.logged_at if last_log else None

    def count_today_logs(self, user_id: int):
        today = datetime.utcnow().date()
        return (
            self.db.query(self.ChallengeLog)
            .filter(
                self.ChallengeLog.user_id == user_id,
                self.ChallengeLog.logged_at >= datetime(today.year, today.month, today.day)
            )
            .count()
        )

    def calculate_user_bonus(self, user_id: int):
        prev_log_date  = self.get_last_log_date(user_id)
        today_log_count = self.count_today_logs(user_id)
        return bonus.calculate(prev_log_date, today_log_count)