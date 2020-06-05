import asyncio
from manager import loop
import db
import manager


class Extractor:
    def __init__(self, db_instance: db.DB, query: str):
        self.id = manager.id_generator.generate()
        self.query = query
        self.db_instance = db_instance
        self.loop = asyncio.get_event_loop()

    def __eq__(self, other):
        return self.id.lower() == other.id or self.query.lower() == other.query.lower()

    def launch(self, total_extractors: int = 1):
        for extractor in range(total_extractors):
            loop.run_light_recurrent_extractor(self.db_instance, self.query)
