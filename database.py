from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME


class Database:

    def __init__(self):
        self.client = MongoClient(MONGO_URI)

        self.db = self.client[DATABASE_NAME]

        self.collection = self.db[COLLECTION_NAME]

        print("MongoDB Connected")


    def add_employee(self, employee_data):
        return self.collection.insert_one(employee_data)


    def get_all_employees(self):
        return list(self.collection.find())


    def delete_employee(self, employee_id):
        return self.collection.delete_one(
            {"employee_id": employee_id}
        )


    def update_employee(self, employee_id, updated_data):
        return self.collection.update_one(
            {"employee_id": employee_id},
            {"$set": updated_data}
        )