from pymongo import MongoClient
from flask import current_app
from bson import ObjectId


class Mongo:
    def __init__(self):
        self.client = None
        self.db = None

    def init_app(self, app):
        uri = app.config.get("MONGO_URI")
        db_name = app.config.get("MONGO_DB_NAME")

        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    
def to_object_id(value: str):
        try:
            return ObjectId(value)
        except Exception:
            return None



mongo = Mongo()


