from flask import Flask
import pandas as pd
import re
from dateutil import parser
from timeit import default_timer as timer
from io import StringIO
from flask import send_file
import db
import config
import flask_graphql
from api import schema


def craft_api(db_instance: db.DB, conf: config.Config):
    app = Flask("Signals")

    app.add_url_rule(
        "/graphql",
        view_func=flask_graphql.GraphQLView.as_view(
            'graphql',
            schema=schema.schema,
            graphiql=True))

    @app.route("/", methods=["GET", "POST"])
    def index():
        return "I'm alive"

    @app.route("/tweets/<string:filename>.csv")
    def get_csv(filename: str):
        valid = re.compile(
            "(s|S)[0-9]{2}-[0-9]{2}-[0-9]{4}(u|U)[0-9]{2}-[0-9]{2}-[0-9]{4}")
        if not valid.match(filename):
            return "please use a valid filename like S{date}U{date}.csv", 500

        chunks = filename.lower().split("u")
        from_str = chunks[0].replace("s", "")
        to_str = chunks[1]

        from_date = parser.parse(from_str)
        to_date = parser.parse(to_str)

        # sample = analytics.QueryDescriptor(from_date=from_date, to_date=to_date)

        start = timer()
        # tweets = analytics.execute_query(db_instance, sample)
        c = db_instance.session.query(db.Tweet) \
            .filter(db.Tweet.created_at >= from_date) \
            .filter(db.Tweet.created_at <= to_date) \
            .statement.compile(db_instance.session.bind)

        print(c, c.params)
        tweets = pd.read_sql(c.string, db_instance.session.bind, params=c.params)
        end = timer()

        print(f"total tweets={len(tweets)} | perform time={end - start}")

        if len(tweets) == 0:
            return "I can't find tweets in this date range, try with other", 404

        data = StringIO()
        tweets.to_csv(data)

        send_file(
            data,
            mimetype="text/csv",
            attachment_filename=f'{filename}.csv',
            as_attachment=True
        )

    return app