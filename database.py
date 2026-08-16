from pymongo import MongoClient

from config import (
    MONGO_URI,
    DATABASE_NAME,
    EMPLOYEE_COLLECTION,
    USER_COLLECTION,
    DEPARTMENT_COLLECTION,
    LEAVE_COLLECTION,
    PAYMENT_COLLECTION
)

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

employees_collection = db[EMPLOYEE_COLLECTION]
users_collection = db[USER_COLLECTION]
departments_collection = db[DEPARTMENT_COLLECTION]
leave_collection = db[LEAVE_COLLECTION]
payments_collection = db[PAYMENT_COLLECTION]


# EMPLOYEE FUNCTIONS


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


# USER FUNCTIONS


def create_user(user_data):
    return users_collection.insert_one(user_data)


def find_user(username):
    return users_collection.find_one(
        {"username": username}
    )

# DEPARTMENT FUNCTIONS


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

def get_employee_by_id(employee_id):

    employee = employees_collection.find_one({
        "employee_id": employee_id
    })

    return employee

def change_password(username, current_password, new_password):

    user = users_collection.find_one({
        "username": username,
        "password": current_password
    })

    if user is None:
        return False

    users_collection.update_one(
        {"username": username},
        {
            "$set": {
                "password": new_password
            }
        }
    )

    return True

def get_employee_statistics():

    total = employees_collection.count_documents({})

    active = employees_collection.count_documents({
        "status": "Active"
    })

    on_leave = employees_collection.count_documents({
        "status": "On Leave"
    })

    resigned = employees_collection.count_documents({
        "status": "Resigned"
    })

    return {
        "total": total,
        "active": active,
        "on_leave": on_leave,
        "resigned": resigned
    }

def search_employees(keyword):

    employees = employees_collection.find({
        "$or": [
            {"employee_id": {"$regex": keyword, "$options": "i"}},
            {"name": {"$regex": keyword, "$options": "i"}},
            {"department": {"$regex": keyword, "$options": "i"}}
        ]
    })

    return list(employees)

# LEAVE FUNCTIONS

def create_leave_request(leave_data):
    return leave_collection.insert_one(leave_data)


def get_employee_leave_requests(employee_id):

    return list(
        leave_collection.find(
            {"employee_id": employee_id}
        )
    )


def get_all_leave_requests():

    return list(
        leave_collection.find()
    )

def update_leave_status(request_id, status):

    from bson.objectid import ObjectId

    # Update leave request
    result = leave_collection.update_one(
        {"_id": ObjectId(request_id)},
        {
            "$set": {
                "status": status
            }
        }
    )

    # If leave is approved
    if status == "Approved":

        leave_request = leave_collection.find_one(
            {"_id": ObjectId(request_id)}
        )

        if leave_request:

            employee_id = leave_request["employee_id"]

            # Change employee status
            employees_collection.update_one(
                {"employee_id": employee_id},
                {
                    "$set": {
                        "status": "On Leave"
                    }
                }
            )

    return result

# PAYMENT FUNCTIONS

def create_payment(payment_data):
    return payments_collection.insert_one(payment_data)


def get_all_payments():
    return list(
        payments_collection.find()
    )


def get_employee_payments(employee_id):
    return list(
        payments_collection.find(
            {"employee_id": employee_id}
        )
    )