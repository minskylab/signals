import graphene as gn
import entities.tweet as tweet


class Query(gn.ObjectType):
    tweets = gn.Field(
        gn.NonNull(gn.List(gn.NonNull(tweet.Tweet))),
        first=gn.Int(default_value=20),
        offset=gn.Int(default_value=0),
        start_date=gn.DateTime(default_value=""),
        end_date=gn.DateTime(default_value=""))

    @staticmethod
    def resolve_tweets(parent: gn.ObjectType, info: gn.ResolveInfo, first: int, offset: int, start_date: gn.DateTime, end_date: gn.DateTime):
        print(first, offset, start_date, end_date)
        return []
