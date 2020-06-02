import graphene as gn


class RootScore(gn.ObjectType):
    root = gn.String(required=True)
    score = gn.Float()
    word = gn.String()


class Topic(gn.ObjectType):
    id = gn.String(required=True)
    roots = gn.NonNull(gn.List(gn.NonNull(gn.Field(RootScore))))
