import db
import config
import analytics
import flask_graphql
from flask import Flask
from flask import request
from io import BytesIO
from flask import send_file
from api import schema
from loguru import logger

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
        q = db.parse_statement_to_query(filename)
        logger.debug(f"from= {q.from_date} | to= {q.to_date}")

        tweets = analytics.run_query_to_df(db_instance, q)

        data = BytesIO(str.encode(tweets.to_csv()))

        if len(tweets) == 0:
            is_pandas = request.args.get("pandas")
            if is_pandas is None:
                return "I can't find tweets in this date range, try with other", 404

        if len(tweets) != 0:
            logger.debug("sampling tweets")
            print(tweets.sample(5))

        return send_file(
            data,
            mimetype="text/csv",
            attachment_filename=f'{filename}.csv',
            as_attachment=True
        )

    return app
