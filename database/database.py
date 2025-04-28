# database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, User, Challenge, Milestone, Reward, Redemption, ChallengeLog, RewardRedemption
from .crud import UserDB, ChallengeDB, RewardDB, RedemptionDB, ChallengeLogDB, StatsDB

import settings


class Database:

    def __init__(self):
        DATABASE_URL = (
            f"postgresql+psycopg2://{settings.database.USERNAME}:{settings.database.PASSWORD}@"
            f"{settings.database.HOST}:{settings.database.PORT}/"
            f"{settings.database.DATABASE}?sslmode={settings.database.SSLMODE}"
        )

        engine = create_engine(url=DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
        Base.metadata.create_all(bind=engine)

        self.db = SessionLocal()

        self.user          = UserDB(self.db, User)
        self.challenge     = ChallengeDB(self.db, Challenge, Milestone)
        self.reward        = RewardDB(self.db, Reward)
        self.redemption    = RedemptionDB(self.db, Redemption)
        self.challenge_log = ChallengeLogDB(self.db, ChallengeLog)
        self.stats         = StatsDB(self.db, ChallengeLog, RewardRedemption)


    def close_session(self):
        self.db.close()


    def delete_user(self, user_id: int):
        challenges = self.db.query(Challenge).filter_by(user_id=user_id).all()

        challenge_ids = [challenge.id for challenge in challenges]
        if challenge_ids:
            self.db.query(Milestone).filter(Milestone.challenge_id.in_(challenge_ids)).delete(synchronize_session=False)

        self.db.query(Challenge).filter_by(user_id=user_id).delete(synchronize_session=False)
        self.db.query(User).filter_by(id=user_id).delete(synchronize_session=False)

        self.db.commit()
        return True