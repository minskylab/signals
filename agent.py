import twint
from datetime import datetime


def run_query(query: str, since: datetime = None, until: datetime = None, limit: int = 10) -> [twint.tweet.tweet]:
    c = twint.Config()
    c.Since = str(since) if not since is None else None
    c.Until = str(until) if not until is None else None
    c.Search = query
    c.Limit = limit
    c.Store_object = True
    c.Hide_output = True
    twint.run.Search(c)

    return twint.run.output.tweets_list
