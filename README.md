# StaffSync

**StaffSync** is a desktop-based Employee Management System built with **Python, Tkinter, and MongoDB**. It provides separate dashboards for administrators and employees, allowing organizations to manage employee records, departments, leave requests, and salary payments.

## Project Overview

StaffSync is designed to simplify basic employee management tasks through a simple graphical user interface.

The system has two main user roles:

* **Admin**
* **Employee**

Administrators can manage employee information, departments, leave requests, and payments, while employees can view their profiles, request leave, view payment records, and change their passwords.

---

##  Features

###  Admin Dashboard

* View employee statistics
* Add employees
* Update employee information
* Delete employees
* Search employees
* Manage departments
* View employee leave requests
* Approve leave requests
* Deny leave requests
* Record employee payments
* Automatically load an employee's salary when recording payment
* Logout

###  Employee Dashboard

* View personal profile
* View employee ID
* View department
* View salary
* View employment status
* Request leave
* View previous leave requests
* View leave request status
* View salary/payment records
* Change password
* Logout

###  Employee Management

Each employee can have:

* Employee ID
* Full name
* Department
* Salary
* Employment status
* Username
* Password

Employee IDs are automatically generated in the format:

```text
EMP001
EMP002
EMP003
```

---

##  Payment Management

Administrators can record employee payments from the Admin Dashboard.

Payment information includes:

* Employee
* Month
* Amount
* Payment status

Payment statuses include:

* Paid
* Pending

Once a payment is recorded, it is stored in MongoDB and can be viewed by the corresponding employee from their dashboard.

---

##  Leave Management

Employees can submit leave requests by providing:

* Leave type
* Start date
* End date
* Reason

Available leave types include:

* Annual Leave
* Sick Leave
* Maternity Leave
* Paternity Leave
* Emergency Leave
* Unpaid Leave

Leave requests initially have a **Pending** status.

Administrators can then:

* Approve the request
* Deny the request

When a leave request is approved, the employee's status is automatically changed to **On Leave**.

---

##  Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Main programming language |
| Tkinter    | Graphical User Interface  |
| MongoDB    | Database                  |
| PyMongo    | Python-MongoDB connection |
| ttk        | Tkinter themed widgets    |

---

##  Project Structure

```text
StaffSync/
│
├── app.py
├── admin.py
├── employee.py
├── database.py
├── config.py
├── login.py
│
├── README.md
│
└── screenshots/
    ├── login.png
    ├── admin-dashboard.png
    ├── employee-management.png
    ├── employee-dashboard.png
    ├── leave-request.png
    └── payment-management.png
```

> The exact filenames may vary depending on the final project structure.

---

# Screenshots

##  Login Page

<!-- Add your login screenshot here -->

![StaffSync Login](screenshots/login.png)

---

##  Admin Dashboard

<!-- Add your admin dashboard screenshot here -->

![Admin Dashboard](screenshots/admin-dashboard.png)

---

##  Employee Management

<!-- Add your employee management screenshot here -->

![Employee Management](screenshots/employee-management.png)

---

##  Employee Dashboard

<!-- Add your employee dashboard screenshot here -->

![Employee Dashboard](screenshots/employee-dashboard.png)

---

##  Leave Request

<!-- Add your leave request screenshot here -->

![Leave Request](screenshots/leave-request.png)

---

##  Payment Management

<!-- Add your payment management screenshot here -->

![Payment Management](screenshots/payment-management.png)

---

#  Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/Jblue254/StaffSync.git
```

Then move into the project directory:

```bash
cd StaffSync
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

Install PyMongo:

```bash
pip install pymongo
```

If the project contains a `requirements.txt` file, you can instead run:

```bash
pip install -r requirements.txt
```

---

## 4. Configure MongoDB

Update your MongoDB connection information in:

```text
config.py
```

The application uses MongoDB to store:

* Employees
* Users
* Departments
* Leave requests
* Payments

---

## 5. Run the Application

Start the login page:

```bash
python login.py
```

From there, users can log in according to their assigned role.

---


---

#  Database Collections

StaffSync uses the following MongoDB collections:

```text
employees
users
departments
leave
payments
```

### Employees

Stores employee information such as:

```text
employee_id
name
department
salary
status
```

### Users

Stores login information:

```text
username
password
role
employee_id
```

### Departments

Stores department information:

```text
name
```

### Leave

Stores employee leave requests:

```text
employee_id
employee_name
leave_type
start_date
end_date
reason
status
```

### Payments

Stores employee payment records:

```text
employee_id
employee_name
month
amount
status
```

---

#  Admin Dashboard Statistics

The Admin Dashboard provides basic employee statistics:

```text
Total Employees
Active Employees
Employees On Leave
Resigned Employees
```

These values are retrieved directly from MongoDB.

---

#  Future Improvements

Possible future improvements include:

* Improved dashboard UI
* Charts and graphs
* Department statistics
* Salary sorting and filtering
* Employee profile pages
* Payment history filtering
* Leave history filtering
* Export employee records
* Export payment reports
* Profile pictures
* Notifications
* Improved form validation

---

#  Adding Screenshots

To add screenshots to the README, place your images inside the `screenshots` folder:

```text
screenshots/
├── login.png
├── admin-dashboard.png
├── employee-management.png
├── employee-dashboard.png
├── leave-request.png
└── payment-management.png
```

Then reference them in Markdown:

```markdown
![Admin Dashboard](screenshots/admin-dashboard.png)
```

---

#  Author

**Japheth Kiprono**

GitHub:

[Jblue254/StaffSync](https://github.com/Jblue254/StaffSync)

---

#  License

This project was created for educational and development purposes.
