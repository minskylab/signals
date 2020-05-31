import sqlalchemy as sqa
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db import tweet
from db import base


class DB:
    def __init__(self, url_conn: str):
        self.url_connection = url_conn

        self.engine: sqa.engine.Engine = sqa.create_engine(self.url_connection)
        base.Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def last_tweet(self) -> tweet.Tweet:
        return self.session.query(tweet.Tweet).order_by(tweet.Tweet.id.desc()).first()

    def save_new_tweet(self, t: tweet.Tweet) -> bool:
        try:
            exists = self.session.query(tweet.Tweet).\
                filter_by(id=t.id).scalar() is not None
            if exists:
                return True
            self.session.add(t)
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
            return False
        return True
