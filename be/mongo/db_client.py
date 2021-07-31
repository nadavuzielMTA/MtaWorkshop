from pymongo import MongoClient


class AtlasMongoClient:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://nadavuziel:QAZqaz123@cluster0.vgwzl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client.get_database("workshop")
