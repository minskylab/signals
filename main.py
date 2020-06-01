# import api
from sources import agent
import datetime
import db
from tqdm import tqdm
import config
import manager
import asyncio
import analytics

if __name__ == "__main__":
    # api.app.run(debug=True)
    conf = config.load_config()

    db_instance = db.DB(conf.postgres_uri)
    principal = manager.Extractor(db_instance, "peru")
    # principal.launch()

    now = datetime.datetime.now()
    from_date = now - datetime.timedelta(hours=1)

    sample = analytics.QueryDescriptor(from_date=from_date, to_date=now)

    tweets = analytics.execute_query(db_instance, sample)
    print(len(tweets))
