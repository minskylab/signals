from sources import agent
import db
from tqdm import tqdm

def run_light_recurrent_extractor(db_instance: db.DB, query: str, max_tweets: int = 100):
    while True:
        tweets = agent.run_query(query, limit=max_tweets)
        print(f"total tweets: {len(tweets)}")

        for tweet in tqdm(tweets):
            db_instance.save_new_tweet(db.convert_tweet(tweet))
