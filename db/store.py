import sqlalchemy as sqa
from sqlalchemy.orm import sessionmaker, Query as SQLQuery

from .tweet import Tweet
from .high import Query
from .base import Base


class DB:
    def __init__(self, url_conn: str):
        self.url_connection = url_conn

        self.engine: sqa.engine.Engine = sqa.create_engine(self.url_connection)
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def last_tweet(self) -> Tweet:
        return self.session.query(Tweet).order_by(Tweet.id.desc()).first()

    def save_new_tweet(self, t: Tweet) -> bool:
        try:
            exists = self.session.query(Tweet).filter_by(id=t.id).scalar() is not None
            if exists:
                return True
            self.session.add(t)
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
            return False
        return True

    def construct_sql_query(self, query: Query) -> SQLQuery:
        q = self.session.query(Tweet)
        q = q.filter(Tweet.created_at >= query.from_date)
        q = q.filter(Tweet.created_at <= query.to_date)

        if query.filter is not None:
            if query.filter.with_mentions is not None:
                for mention in query.filter.with_mentions:
                    q = q.filter(mention in Tweet.mentions)
            if query.filter.usernames is not None:
                for username in query.filter.usernames:
                    q = q.filter(Tweet.username == username)
            if query.filter.with_reply_to is not None:
                for user_ref in query.filter.with_reply_to:
                    q = q.filter(user_ref in Tweet.reply_to)
            if query.filter.words is not None:
                for word in query.filter.words:
                    q = q.filter(word in Tweet.tweet)
            if query.filter.with_retweets_greater_than is not None:
                q = q.filter(Tweet.retweets_count >= query.filter.with_retweets_greater_than)
            if query.filter.with_retweets_less_than is not None:
                q = q.filter(Tweet.retweets_count <= query.filter.with_retweets_less_than)
            if query.filter.with_retweets_equals_to is not None:
                q = q.filter(Tweet.retweets_count == query.filter.with_retweets_equals_to)
        return q

    def get_tweets(self, query: Query) -> [Tweet]:
        q = self.construct_sql_query(query)
        tweets = q.all()
        return tweets
