# database/crud/stats.py

from .base import BaseDB


class StatsDB(BaseDB):

    def __init__(self, db, ChallengeLog, RewardRedemption):
        super().__init__(db)
        self.ChallengeLog = ChallengeLog
        self.RewardRedemption = RewardRedemption

    def count_completed_challenges(self, user_id: int) -> int:
        return self.db.query(self.ChallengeLog).filter(
            self.ChallengeLog.user_id == user_id,
            self.ChallengeLog.status == "completed"
        ).count()

    def count_total_days_logged(self, user_id: int) -> int:
        return self.db.query(self.ChallengeLog.day).filter(
            self.ChallengeLog.user_id == user_id
        ).distinct().count()

    def count_redeemed_rewards(self, user_id: int) -> int:
        return self.db.query(self.RewardRedemption).filter(
            self.RewardRedemption.user_id == user_id
        ).count()

    def get_current_streak(self, user_id: int) -> int:
        logs = self.db.query(self.ChallengeLog).filter(
            self.ChallengeLog.user_id == user_id
        ).order_by(self.ChallengeLog.timestamp.desc()).all()

        if not logs:
            return 0

        streak = 0
        previous_day = None

        for log in logs:
            log_day = log.timestamp.date()

            if previous_day is None:
                previous_day = log_day
                streak += 1
                continue

            if (previous_day - log_day).days == 1:
                streak += 1
                previous_day = log_day
            else:
                break

        return streak