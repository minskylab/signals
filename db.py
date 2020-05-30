import sqlalchemy as sqa

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Tweet(Base):
    id = sqa.Column(sqa.String, primary_key=True, nullable=False)
    conversation_id = sqa.Column(sqa.String, nullable=False)
    created_at = sqa.Column(sqa.DateTime, nullable=False)
    timezone = sqa.Column(sqa.Integer, nullable=False)
    user_id = sqa.Column(sqa.String, nullable=False)
    tweet = sqa.Column(sqa.Text, nullable=False)
    _mentions = sqa.Column(sqa.String, nullable=False, default="")
    _hashtags = sqa.Column(sqa.String, nullable=False, default="")
    _cashtags = sqa.Column(sqa.String, nullable=False, default="")
    _reply_to = sqa.Column(sqa.String, nullable=False, default="")
    timezone = sqa.Column(sqa.Integer)
    timezone = sqa.Column(sqa.Integer)

    @property
    def mentions(self) -> [str]:
        return self._mentions.split(",")

    @mentions.setter
    def mentions(self, value: [str]):
        self._mentions = ",".join(value)

    @property
    def hashtags(self) -> [str]:
        return self._hashtags.split(",")

    @hashtags.setter
    def hashtags(self, value: [str]):
        self._hashtags = ",".join(value)

    @property
    def cashtags(self) -> [str]:
        return self._cashtags.split(",")

    @cashtags.setter
    def cashtags(self, value: [str]):
        self._cashtags = ",".join(value)

    @property
    def reply_to(self) -> [str]:
        return self._reply_to.split(",")

    @reply_to.setter
    def reply_to(self, value: [str]):
        self._reply_to = ",".join(value)


class DB:
    def __init__(self, url_conn: str):
        self.url_connection = url_conn

        self.engine: sqa.engine.Engine = None
        self.engine = sqa.create_engine(self.url_connection)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def save_new_tweet(self, tweet: Tweet) -> bool:
        try:
            self.session.add(tweet)
        except:
            return False
        return True
