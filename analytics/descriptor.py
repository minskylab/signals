from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta


@dataclass
class QueryFilter:
    words: [str] = None
    usernames: [str] = None
    with_mentions: [str] = None
    with_reply_to: [str] = None
    with_retweets_greater_than: int = None
    with_retweets_less_than: int = None
    with_retweets_equals_to: int = None


@dataclass
class QueryDescriptor:
    from_date: datetime
    to_date: datetime
    filter: QueryFilter = None


def get_recent_sample_query() -> QueryDescriptor:
    from_date = datetime.now() - timedelta(hours=1)
    to_date = datetime.now()
    return QueryDescriptor(from_date, to_date)
