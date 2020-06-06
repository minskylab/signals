import pandas as pd
import networkx as nx


def fix_tweet(message:str) -> str:
    words = [w for w in message.split(" ") if not w.startswith("http")]
    words = [w for w in words if len(w) < 12]
    return " ".join(words).replace("\n", "").strip()


def dataframe_tweets_to_graph(tweets: pd.DataFrame, relation_by: str = "reply_to") -> nx.DiGraph:
    df = tweets.copy()
    df["tweet"] = df["tweet"].map(lambda t: str(t))
    df["tweet"] = df["tweet"].map(fix_tweet)
    g = nx.DiGraph()

    for i, tweet in df.iterrows():
        if relation_by not in tweet.keys():
            raise BaseException("please, use a correct key")
        related_tweets = tweet[relation_by]

        for r in related_tweets:
            g.add_edge(tweet["username"], r["username"], tweet=tweet["tweet"], likes=tweet["likes_count"])

    valid_nodes = []
    for node in g.nodes:
        if g.degree[node] > 2:
            valid_nodes.append(node)

    g_valid: nx.DiGraph = g.subgraph(valid_nodes)

    print(f"valid nodes: {len(g.nodes)} | valid edges: {len(g_valid.edges)}")

    return g_valid
