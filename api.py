import query as q
import graphene as gn

# from flask import Flask
# app = Flask("Signals")
# def

schema = gn.Schema(query=q.Query)
print(schema.execute("{tweets {id}}"))
