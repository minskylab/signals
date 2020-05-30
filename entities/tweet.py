import graphene as gn

"""Tweet represents an object of graphql schema
"""


class Tweet(gn.ObjectType):
    id = gn.String(required=True)
    conversation_id = gn.String(required=True)
    created_at = gn.DateTime(required=True)
    timezone = gn.Int(required=True)
    user_id = gn.String(required=True)
    tweet = gn.String()
    mentions = gn.NonNull(gn.List(gn.NonNull(gn.String)))
    hashtags = gn.NonNull(gn.List(gn.NonNull(gn.String)))
    cashtags = gn.NonNull(gn.List(gn.NonNull(gn.String)))
    reply_to = gn.NonNull(gn.List(gn.NonNull(gn.String)))
    retweets_count = gn.Int()
    replies_count = gn.Int()
