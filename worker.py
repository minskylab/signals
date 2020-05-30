import twint
from datetime import datetime

c = twint.Config()
c.Since = str(datetime(2020, 5, 28, 0))
c.Until = str(datetime(2020, 5, 29, 0))
c.Search = "peru"
c.Elasticsearch = "localhost:9200"
c.Limit = 10

twint.run.Search(c)
