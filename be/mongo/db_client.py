from pymongo import MongoClient


class AtlasMongoClient:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.admin
