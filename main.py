# import api
from sources import agent
import datetime
import db
from tqdm import tqdm
import config

if __name__ == "__main__":
    # api.app.run(debug=True)
    conf = config.load_config()

    db_instance = db.DB(conf.postgres_uri)
    last = db_instance.last_tweet()

    since = last.created_at - \
        datetime.timedelta(minutes=5, hours=5)  # UTC-5 -5m
    since = since.replace(second=0, microsecond=0)
    until = datetime.datetime.now().replace(second=0, microsecond=0)

    print(f"since = {since}")

    max_tweets = 100

    while not last.created_at < until:
        tweets = agent.run_query(
            "peru",
            since=since,
            # until=until,
            limit=max_tweets)

        print(f"total tweets: {len(tweets)}")

        for tweet in tqdm(tweets):
            db_instance.save_new_tweet(db.convert_tweet(tweet))

        last = db_instance.last_tweet()
        since = last.created_at - \
            datetime.timedelta(minutes=5, hours=5)  # UTC-5 -5m
        since = since.replace(second=0, microsecond=0)
