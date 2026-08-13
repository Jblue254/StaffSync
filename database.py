from pymongo import MongoClient

from config import (
    MONGO_URI,
    DATABASE_NAME,
    EMPLOYEE_COLLECTION,
    USER_COLLECTION,
    DEPARTMENT_COLLECTION
)

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

employees_collection = db[EMPLOYEE_COLLECTION]
users_collection = db[USER_COLLECTION]
departments_collection = db[DEPARTMENT_COLLECTION]


# =========================
# EMPLOYEE FUNCTIONS
# =========================

def add_employee(employee_data):
    return employees_collection.insert_one(employee_data)


def get_all_employees():
    return list(employees_collection.find())


def update_employee(employee_id, updated_data):
    return employees_collection.update_one(
        {"employee_id": employee_id},
        {"$set": updated_data}
    )


def delete_employee(employee_id):
    return employees_collection.delete_one(
        {"employee_id": employee_id}
    )


def generate_employee_id():

    last_employee = employees_collection.find_one(
        {},
        sort=[("employee_id", -1)]
    )

    if last_employee is None:
        return "EMP001"

    last_id = last_employee["employee_id"]

    number = int(last_id.replace("EMP", ""))

    new_number = number + 1

    return f"EMP{new_number:03d}"


# =========================
# USER FUNCTIONS
# =========================

def create_user(user_data):
    return users_collection.insert_one(user_data)


def find_user(username):
    return users_collection.find_one(
        {"username": username}
    )


# =========================
# DEPARTMENT FUNCTIONS
# =========================

def add_department(department_data):
    return departments_collection.insert_one(
        department_data
    )


def get_all_departments():
    return list(
        departments_collection.find()
    )


def delete_department(department_name):
    return departments_collection.delete_one(
        {"name": department_name}
    )

def login_user(username, password):

    user = users_collection.find_one({
        "username": username,
        "password": password
    })

    return user