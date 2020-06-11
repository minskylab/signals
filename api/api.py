from db import DB, parse_statement_to_query
from flask import request
from loguru import logger
from analytics import run_query_to_df
from pandas import DataFrame
from tempfile import NamedTemporaryFile


def dataframe_to_csv_file(df: DataFrame) -> NamedTemporaryFile:
    t_file = NamedTemporaryFile(mode="r+")
    csv = df.to_csv(chunksize=int(30e3))
    # testing a <chuncked> exportation
    _ = t_file.write(csv)
    t_file.seek(0)
    return t_file


def export_csv_from_statement(db_instance: DB, statement: str, for_pandas=False) -> NamedTemporaryFile:
    q = parse_statement_to_query(statement)

    timezone = request.args.get("timezone", type=str)
    if timezone is not None:
        q.apply_timezone(timezone)

    logger.debug(f"from = {q.from_date} | to = {q.to_date}")

    tweets = run_query_to_df(db_instance, q)

    buffer = dataframe_to_csv_file(tweets)

    if len(tweets) == 0:
        if for_pandas is None or for_pandas == "":
            raise BaseException("I can't find tweets in this date range, try with other")
    else:
        logger.debug("sampling tweets")
        logger.debug(tweets.sample(3))

    return buffer
