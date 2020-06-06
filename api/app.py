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
from .api import export_csv_from_statement


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

        is_for_pandas = request.args.get("pandas", type=str)

        file = export_csv_from_statement(db_instance, filename, for_pandas=is_for_pandas)

        return send_file(
            file.name,
            mimetype="text/csv",
            attachment_filename=f'{filename}.csv',
            as_attachment=True
        )

    return app
