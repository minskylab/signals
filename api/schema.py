from api import query
import graphene as gn

schema = gn.Schema(query=query.Query)
