from flask import Flask
import flask_graphql
import flask
import schema

app = Flask("Signals")

app.add_url_rule(
    "/graphql",
    view_func=flask_graphql.GraphQLView.as_view(
        'graphql',
        schema=schema.schema,
        graphiql=True))


@app.route('/', methods=["GET", "POST"])
def index():
    return "I'm alive"
