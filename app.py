import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    add_employee as save_employee,
    get_all_employees,
    generate_employee_id,
    create_user,
    update_employee as update_employee_database,
    delete_employee as delete_employee_database
)

# FUNCTIONS
def select_employee(event):

    selected = employee_table.selection()

    if not selected:
        return

    employee = employee_table.item(selected[0])

    values = employee["values"]

    name_entry.delete(0, tk.END)
    name_entry.insert(0, values[1])

    department_combobox.set(values[2])

    salary_entry.delete(0, tk.END)
    salary_entry.insert(0, values[3])

    status_combobox.set(values[4])



def add_employee():

    name = name_entry.get().strip()
    department = department_combobox.get()
    salary = salary_entry.get().strip()
    status = status_combobox.get()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not name or not department or not salary or not username or not password:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )
        return

    employee_id = generate_employee_id()

    employee_data = {
        "employee_id": employee_id,
        "name": name,
        "department": department,
        "salary": salary,
        "status": status
    }

    user_data = {
        "username": username,
        "password": password,
        "role": "employee",
        "employee_id": employee_id
    }

    save_employee(employee_data)

    create_user(user_data)

    load_employees()

    clear_fields()

    messagebox.showinfo(
        "Success",
        f"Employee added successfully!\n\nEmployee ID: {employee_id}"
    )

def update_employee():

    selected = employee_table.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select an employee from the table."
        )
        return

    employee = employee_table.item(selected[0])

    employee_id = employee["values"][0]

    name = name_entry.get().strip()
    department = department_combobox.get()
    salary = salary_entry.get().strip()
    status = status_combobox.get()

    if not name or not department or not salary:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all employee fields."
        )
        return

    updated_data = {
        "name": name,
        "department": department,
        "salary": salary,
        "status": status
    }

    update_employee_database(
        employee_id,
        updated_data
    )

    load_employees()

    clear_fields()

    messagebox.showinfo(
        "Success",
        f"Employee {employee_id} updated successfully."
    )


def delete_employee():

    selected = employee_table.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select an employee from the table."
        )
        return

    employee = employee_table.item(selected[0])

    employee_id = employee["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete {employee_id}?"
    )

    if not confirm:
        return

    delete_employee_database(employee_id)

    load_employees()

    clear_fields()

    messagebox.showinfo(
        "Success",
        f"Employee {employee_id} deleted successfully."
    )


def clear_fields():

    name_entry.delete(0, tk.END)

    department_combobox.current(0)

    salary_entry.delete(0, tk.END)

    status_combobox.current(0)

    username_entry.delete(0, tk.END)

    password_entry.delete(0, tk.END)


def load_employees():

    # Remove existing rows from the table
    employee_table.delete(
        *employee_table.get_children()
    )

    # Get employees from MongoDB
    employees = get_all_employees()

    # Display employees in the table
    for employee in employees:

        employee_table.insert("","end",
            values=(
                employee["employee_id"],
                employee["name"],
                employee["department"],
                employee["salary"],
                employee["status"]
            )
        )

def logout():
    root.destroy()

    import login



# MAIN WINDOW


root = tk.Tk()

root.title("Employee Management System")
root.geometry("1200x700")
root.resizable(False, False)

# TITLE

title_label = tk.Label(root,text="EMPLOYEE MANAGEMENT SYSTEM",font=("Arial", 20, "bold"))
title_label.pack(pady=10)

# MAIN FRAME


main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# FORM FRAME

form_frame = tk.LabelFrame(main_frame,text="Employee Info",padx=10,pady=10)
form_frame.pack(side="left", fill="y")


# Full Name
tk.Label(form_frame,text="Full Name").grid(row=2, column=0, sticky="w")
name_entry = tk.Entry(form_frame,width=30)
name_entry.grid(row=3,column=0,pady=5)

# Department
tk.Label(form_frame,text="Department").grid(row=4, column=0, sticky="w")

department_combobox = ttk.Combobox(form_frame,
    values=[
        "IT",
        "HR",
        "Finance",
        "Marketing",
        "Sales",
        "Operations"],width=27,state="readonly")
department_combobox.grid(row=5,column=0,pady=5)

department_combobox.current(0)

# Salary
tk.Label(form_frame,text="Salary").grid(row=6, column=0, sticky="w")

salary_entry = tk.Entry(form_frame, width=30)
salary_entry.grid(row=7, column=0, pady=5)

# Status
tk.Label(form_frame,text="Status").grid(row=8, column=0, sticky="w")
status_combobox = ttk.Combobox(form_frame,values=["Active", "On Leave", "Resigned"],width=27)

status_combobox.grid(row=9, column=0, pady=5)
status_combobox.current(0)

# Username

tk.Label(form_frame,text="Username").grid(row=10, column=0, sticky="w")
username_entry = tk.Entry(form_frame,width=30)
username_entry.grid(row=11,column=0,pady=5)
# Temporary Password

tk.Label(form_frame,text="Temporary Password").grid(row=12, column=0, sticky="w")

password_entry = tk.Entry(form_frame,width=30,show="*")

password_entry.grid(row=13,column=0,pady=5)

# Buttons
add_button = tk.Button(form_frame,text="Add Employee",width=25,command=add_employee)
add_button.grid(row=14, column=0, pady=10)

update_button = tk.Button(form_frame,text="Update Employee",width=25,command=update_employee)
update_button.grid(row=15, column=0, pady=5)

delete_button = tk.Button(form_frame,text="Delete Employee",width=25,command=delete_employee)
delete_button.grid(row=16, column=0, pady=5)

logout_button = tk.Button(form_frame,text="Logout",width=25,command=logout)
logout_button.grid(row=17,column=0,pady=15)

# TABLE FRAME


table_frame = tk.LabelFrame(
    main_frame,
    text="Employee Records",
    padx=10,
    pady=10
)

table_frame.pack(
    side="right",
    fill="both",
    expand=True
)

# Table Columns
columns = (
    "ID",
    "Name",
    "Department",
    "Salary",
    "Status"
)

employee_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)
employee_table.bind(
    "<<TreeviewSelect>>",
    select_employee
)

for col in columns:
    employee_table.heading(col, text=col)
    employee_table.column(col, width=140)

# Scrollbar
scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=employee_table.yview
)

employee_table.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(side="right", fill="y")
employee_table.pack(fill="both", expand=True)


# Load employees from MongoDB
load_employees()

# RUN APPLICATION

if __name__ == "__main__":
    root.mainloop()