import manager
from db import DB
from enum import Enum
from typing import Dict
from threading import Thread


class ExtractorStatus(Enum):
    IDLE = 0
    RUNNING = 1
    DEAD = 2


class Manager:
    def __init__(self, db: DB):
        self.bd: DB = db
        self.extractors: [manager.Extractor] = []
        self.statues: Dict[str, ExtractorStatus] = {}
        self.threads: Dict[str, Thread] = {}

    def register_new_extractor(self, extractor: manager.Extractor):
        self.extractors.append(extractor)
        self.statues[extractor.id] = ExtractorStatus.IDLE

    def launch_extractors(self):
        for extractor in self.extractors:
            if self.statues[extractor.id] == ExtractorStatus.IDLE:
                light_t = Thread(target=extractor.launch)
                self.threads[extractor.id] = light_t
                self.threads[extractor.id].start()
                self.statues[extractor.id] = ExtractorStatus.RUNNING
                print(f"Extractor (id={extractor.id}) launched")
