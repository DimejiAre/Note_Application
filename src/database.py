import pymongo


class Database(object):

    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        """method to create Databse 'Notes' in mongodb """
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["Notes"]

    @staticmethod
    def insert(collection, data):
        """method to insert data into mongodb database"""
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, data):
        """method to retrieve multiple items from mongodb database"""
        return Database.DATABASE[collection].find(data)

    @staticmethod
    def find_one(collection, data):
        """method to retrieve single item from mongodb database"""
        return Database.DATABASE[collection].find_one(data)

    @staticmethod
    def delete(collection, data):
        """method to delete an item from mongodb database"""
        Database.DATABASE[collection].remove(data)

    @staticmethod
    def update(collection, match, data):
        """method to update entry on mongodb database"""
        Database.DATABASE[collection].update_one(match, data)


