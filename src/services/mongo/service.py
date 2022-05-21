from src.app.plugins import mongo


class MongoService:
    def __init__(self):
        self.db = mongo.flask_db

    def create(self, table, data):
        self.db[table] = data

    def get(self, table):
        return self.db[table].find()
