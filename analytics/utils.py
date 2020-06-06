import pandas as pd
from db import Query, DB, Tweet, rows
from timeit import default_timer as timer
from loguru import logger


def run_query_to_df(db_instance: DB, query: Query) -> pd.DataFrame:
    start = timer()

    q = db_instance.construct_sql_query(query)

    c = q.statement.compile(db_instance.session.bind)
    tweets = pd.read_sql(c.string, db_instance.session.bind, params=c.params)
    tweets = tweets.rename(columns=rows)

    end = timer()

    logger.debug(f"found tweets = {len(tweets)} | perform time = {end - start}")

    return tweets
