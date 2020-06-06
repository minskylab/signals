from db import DB, Query, Tweet
from analytics import run_query_to_df
from .graph import dataframe_tweets_to_graph
from networkx import DiGraph, write_gexf, generate_gexf
from typing import Generator
from tempfile import SpooledTemporaryFile, TemporaryFile


class Processor:
    def __init__(self, db_instance: DB):
        self.db = db_instance

    def graph_from_query(self, query: Query, with_relation: str = "reply_to") -> DiGraph:
        df = run_query_to_df(db_instance=self.db, query=query)
        graph = dataframe_tweets_to_graph(df, relation_by=with_relation)
        return graph

    def generator_gexf_from_query(self, query: Query, with_relation: str = "reply_to") -> Generator[str]:
        graph = self.graph_from_query(query, with_relation=with_relation)
        return generate_gexf(graph)

    def file_gexf_from_query(self, query: Query, with_relation: str = "reply_to") -> TemporaryFile:
        file = SpooledTemporaryFile(max_size=int(1e6), mode="rwb+")
        graph = self.graph_from_query(query, with_relation=with_relation)
        write_gexf(graph, file)
        return file

    # def yaml_from_query(self, query: Query):
    #     graph = self.graph_from_query(query, with_relation=with_relation)
