import re
import datetime
from dataclasses import dataclass
from datetime import timedelta
from dateutil import parser
from typing import Optional, Dict
from loguru import logger


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


def extract_expression(statement: str, name: str) -> str:
    expression: str = ""
    for j in range(statement.index(name)+1, len(statement)):
        c = statement[j]
        if not c.isdigit():
            if c not in "-T()":
                break
        expression += c
    return expression


def parse_statement_to_query(statement: str) -> Query:
    invalid_statement = BaseException("please use a valid statement like S{date}U{date} (TODO: to complete it)")

    statement = statement.lower().strip()
    statement = statement.replace("t", "T")

    if len(statement) == 0:
        raise invalid_statement

    since: Optional[datetime.datetime] = None
    until: Optional[datetime.datetime] = None

    if "s" in statement:
        expression = extract_expression(statement, "s")
        logger.debug(expression)
        since = parser.parse(expression)

    if "u" in statement:
        expression = extract_expression(statement, "u")
        logger.debug(expression)
        until = parser.parse(expression)

    if since is not None and until is not None:
        from_date = since.replace(microsecond=0)
        to_date = until.replace(microsecond=0)

        return Query(from_date, to_date)

    # block-block-blockTblock:block:block
    block_4: str = """(\d{1,4}|(\(\d{1,4}-\d{1,4}\)))"""
    block_2: str = """(\d{1,2}|(\(\d{1,2}-\d{1,2}\)))"""

    little_l = re.compile(block_4 + "-" + block_2 + "-" + block_4 + "T" + block_2 + ":" + block_2 + ":" + block_2)

    logger.debug(statement)

    if little_l.match(statement) is None:
        raise invalid_statement

    blocks = re.compile(block_4).findall(statement)

    if len(blocks) == 0:
        raise invalid_statement

    blocks: [str] = [b[0] for b in blocks]  # first of first

    logger.debug(blocks)

    since_map: Dict[int, int] = {}
    until_map = {}
    for i, block in enumerate(blocks):
        s_str: str = block
        u_str: str = block

        if "(" in block:
            chunks = block.split("-")
            logger.debug(chunks)
            s_str = chunks[0].replace("(", "").strip()
            u_str = chunks[1].replace(")", "").strip()

        since_map[i] = int(s_str)
        until_map[i] = int(u_str)

    since = datetime.datetime(*list(since_map.values()))
    until = datetime.datetime(*list(until_map.values()))

    from_date = since.replace(microsecond=0)
    to_date = until.replace( microsecond=0)

    return Query(from_date, to_date)
