import db
import config
import analytics
import flask_graphql
from flask import Flask
from flask import request
from io import StringIO
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
        if conf.root_token != "":
            token = request.args.get("token", type=str)
            if token is None:
                return "You need to pass a valid auth token", 401

            logger.debug(token)
            if token != conf.root_token: # TODO: Update to a dynamic token
                return "Invalid auth token", 401

        q = db.parse_statement_to_query(filename)

        timezone = request.args.get("timezone", type=str)
        if timezone is not None:
            q.apply_timezone(timezone)

        logger.debug(f"from = {q.from_date} | to = {q.to_date}")

        tweets = analytics.run_query_to_df(db_instance, q)

        buffer = StringIO()

        tweets.to_csv(buffer)
        buffer.seek(0)
        
        if len(tweets) == 0:
            is_pandas = request.args.get("pandas", type=str)
            if is_pandas is None or is_pandas == "":
                return "I can't find tweets in this date range, try with other", 404
        else:
            logger.debug("sampling tweets")
            logger.debug(tweets.sample(3))

        return send_file(
            buffer,
            mimetype="text/csv",
            attachment_filename=f'{filename}.csv',
            as_attachment=True
        )

    return app
