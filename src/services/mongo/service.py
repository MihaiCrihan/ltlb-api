from src.app.plugins import mongo


class MongoService:
    def __init__(self):
        self.db = mongo.flask_db

    def create(self, table, data):
        self.db[table].insert_one(data)

    def create_or_update(self, table, data):
        item = self.find_one(table, data['id'])

        if item:
            print('exists', data['id'])
            self.db[table].update_one({"_id": item['_id']}, {'$set': {**data}})
            return

        self.db[table].insert_one(data)

    def drop(self, table):
        self.db[table].drop()

    def get(self, table):
        return self.db[table].find()

    def find_one(self, table, id):
        return self.db[table].find_one({"id": id})



