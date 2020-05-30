import query as q
import graphene as gn

schema = gn.Schema(query=q.Query)
