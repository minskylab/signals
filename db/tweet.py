import sqlalchemy as sqa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from db import base


class Tweet(base.Base):
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
