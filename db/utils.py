import twint
from db import tweet
from datetime import datetime


def convert_tweet(t: twint.tweet.tweet) -> tweet.Tweet:
    replies_to: [str] = []
    if type(t.reply_to) is list:
        for rep in t.reply_to:
            if type(rep) is dict:
                if "username" in rep:
                    replies_to.append(rep["username"] or "")

    created_at = datetime.utcfromtimestamp(int(t.datetime)/1000)

    return tweet.Tweet(
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
