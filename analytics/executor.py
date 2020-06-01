from analytics import QueryDescriptor
from db import DB, Tweet


def execute_query(db_instance: DB, query: QueryDescriptor) -> [Tweet]:
    tweets = db_instance.session.query(Tweet)\
        .filter(Tweet.created_at >= query.from_date)\
        .filter(Tweet.created_at <= query.to_date)\
        .all()
    return tweets
