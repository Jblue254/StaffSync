from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI)

            # Test the connection
            self.client.admin.command("ping")

            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]

            print("MongoDB Connected Successfully")

        except Exception as error:
            print("Connection Failed")
            print(error)