import asyncio
from manager import loop
import db
import random
import manager


class Extractor:
    def __init__(self, db_instance: db.DB, query: str):
        self.id = manager.ulid.generate()
        self.query = query
        self.db_instance = db_instance
        self.loop = asyncio.get_event_loop()

    def launch(self, total_extractors: int = 1):
        loop.run_light_recurrent_extractor(self.db_instance, self.query)
