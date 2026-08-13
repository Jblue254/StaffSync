import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    add_employee as save_employee,
    get_all_employees,
    generate_employee_id,
    create_user
)

# FUNCTIONS


def add_employee():
    pass


def update_employee():
    pass


def delete_employee():
    pass


def clear_fields():
    pass


def load_employees():
    pass



# MAIN WINDOW


root = tk.Tk()

root.title("Employee Management System")
root.geometry("1200x700")
root.resizable(False, False)

# TITLE


title_label = tk.Label(
    root,
    text="EMPLOYEE MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=10)

# MAIN FRAME


main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# FORM FRAME


form_frame = tk.LabelFrame(
    main_frame,
    text="Employee Info",
    padx=10,
    pady=10
)

form_frame.pack(side="left", fill="y")


# Full Name
tk.Label(
    form_frame,
    text="Full Name"
).grid(row=2, column=0, sticky="w")

name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=3, column=0, pady=5)

# Department
tk.Label(
    form_frame,
    text="Department"
).grid(row=4, column=0, sticky="w")

department_combobox = ttk.Combobox(
    form_frame,
    values=[
        "IT",
        "HR",
        "Finance",
        "Marketing",
        "Sales",
        "Operations"
    ],
    width=27,
    state="readonly"
)

department_combobox.grid(
    row=5,
    column=0,
    pady=5
)

department_combobox.current(0)

# Salary
tk.Label(
    form_frame,
    text="Salary"
).grid(row=6, column=0, sticky="w")

salary_entry = tk.Entry(form_frame, width=30)
salary_entry.grid(row=7, column=0, pady=5)

# Status
tk.Label(
    form_frame,
    text="Status"
).grid(row=8, column=0, sticky="w")

status_combobox = ttk.Combobox(
    form_frame,
    values=["Active", "On Leave", "Resigned"],
    width=27
)

status_combobox.grid(row=9, column=0, pady=5)
status_combobox.current(0)

# Buttons
add_button = tk.Button(
    form_frame,
    text="Add Employee",
    width=25,
    command=add_employee
)

add_button.grid(row=10, column=0, pady=10)

update_button = tk.Button(
    form_frame,
    text="Update Employee",
    width=25,
    command=update_employee
)

update_button.grid(row=11, column=0, pady=5)

delete_button = tk.Button(
    form_frame,
    text="Delete Employee",
    width=25,
    command=delete_employee
)

delete_button.grid(row=12, column=0, pady=5)

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

# Sample Data
employee_table.insert(
    "",
    "end",
    values=(
        "EMP001",
        "John Doe",
        "IT",
        "50000",
        "Active"
    )
)


# RUN APPLICATION


root.mainloop()