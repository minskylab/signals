import sqlalchemy as sqa

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import twint

Base = declarative_base()


class Tweet(Base):
    __tablename__ = "tweets_table"

    id = sqa.Column(sqa.String, primary_key=True, nullable=False)
    username = sqa.Column(sqa.String)
    conversation_id = sqa.Column(sqa.String, nullable=False)
    created_at = sqa.Column(sqa.DateTime, nullable=False)
    timezone = sqa.Column(sqa.Integer, nullable=False)
    user_id = sqa.Column(sqa.String, nullable=False)
    tweet = sqa.Column(sqa.Text, nullable=False)
    _mentions = sqa.Column(sqa.String, nullable=False, default="")
    _hashtags = sqa.Column(sqa.String, nullable=False, default="")
    _cashtags = sqa.Column(sqa.String, nullable=False, default="")
    _reply_to = sqa.Column(sqa.String, nullable=False, default="")
    retweets_count = sqa.Column(sqa.Integer)
    replies_count = sqa.Column(sqa.Integer)

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


def convert_tweet(t: twint.tweet.tweet) -> Tweet:
    replies_to: [str] = []
    if type(t.reply_to) is list:
        for rep in t.reply_to:
            if type(rep) is dict:
                if "username" in rep:
                    replies_to.append(rep["username"] or "")

    created_at = datetime.utcfromtimestamp(int(t.datetime)/1000)

    return Tweet(
        id=str(t.id),
        username=str(t.username),
        conversation_id=str(t.conversation_id),
        created_at=created_at,
        timezone=t.timezone,
        user_id=t.user_id,
        tweet=t.tweet,
        _mentions=t.mentions,
        _hashtags=t.hashtags,
        _cashtags=t.cashtags,
        _reply_to=replies_to,
        retweets_count=t.retweets_count,
        replies_count=t.replies_count
    )


class DB:
    def __init__(self, url_conn: str):
        self.url_connection = url_conn

        self.engine: sqa.engine.Engine = sqa.create_engine(self.url_connection)
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def save_new_tweet(self, tweet: Tweet) -> bool:
        try:
            exists = self.session.query(Tweet).filter_by(
                id=tweet.id).scalar() is not None
            if exists:
                return True
            self.session.add(tweet)
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
            return False
        return True
