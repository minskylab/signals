# import api
from sources import agent
import datetime
import db
from tqdm import tqdm
import config

if __name__ == "__main__":
    # api.app.run(debug=True)
    conf = config.load_config()

    since = datetime.datetime.now() - datetime.timedelta(hours=1)
    since = since.replace(second=0, microsecond=0)
    print(f"since = {since}")
    tweets = agent.run_query("peru", since=since, limit=-1)
    print(f"total tweets: {len(tweets)}")

    db_instance = db.DB(conf.postgres_uri)
    for tweet in tqdm(tweets):
        t = db.convert_tweet(tweet)
        db_instance.save_new_tweet(t)
