import re
from dataclasses import dataclass
import datetime
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
class Query:
    from_date: datetime.datetime
    to_date: datetime.datetime
    filter: QueryFilter = None


def get_recent_sample_query() -> Query:
    from_date = datetime.datetime.now() - timedelta(hours=1)
    to_date = datetime.datetime.now()
    return Query(from_date, to_date)


def parse_statement_to_query(statement: str) -> Query:
    valid = re.compile("(s|S)[0-9]{2}-[0-9]{2}-[0-9]{4}(u|U)[0-9]{2}-[0-9]{2}-[0-9]{4}")
    if not valid.match(statement):
        raise BaseException("please use a valid filename like S{date}U{date}.csv")

    chunks = statement.lower().split("u")
    from_str = chunks[0].replace("s", "")
    to_str = chunks[1]

    from_date = datetime.datetime.strptime(from_str, "%d-%m-%Y")
    to_date = datetime.datetime.strptime(to_str, "%d-%m-%Y")

    from_date = from_date.replace(microsecond=0)
    to_date = to_date.replace( microsecond=0)

    return Query(from_date, to_date)
