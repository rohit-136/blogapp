import os

__author__ = "Rohit Rao"

import pymongo



class Database(object):
    #URI= "mongodb://127.0.0.1:27017"
    URI= os.environ.get("MONGODB_URI")
    DATABASE="myDb"

    @staticmethod
    def initialise():
        client=pymongo.MongoClient("mongodb://host/db_name")
        #Database.DATABASE=client['Python']
        Database.DATABASE=client.get_default_database()

    @staticmethod
    def insert(collection,data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
