import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    get_employee_statistics,
    get_all_leave_requests,
    update_leave_status,
    get_all_employees,
    create_payment
)

# FUNCTIONS

def load_payment_employees():

    employees = get_all_employees()

    employee_ids = []

    for employee in employees:

        employee_ids.append(
            employee["employee_id"]
        )

    payment_employee_combobox["values"] = employee_ids

    if employee_ids:
        payment_employee_combobox.current(0)

def open_employee_management():

    root.destroy()

    import app


def logout():

    root.destroy()

    import login

# LEAVE REQUEST FUNCTIONS

def load_leave_requests():

    # Clear existing rows
    leave_table.delete(
        *leave_table.get_children()
    )

    # Get all requests from MongoDB
    requests = get_all_leave_requests()

    # Add requests to table
    for request in requests:

        leave_table.insert(
            "",
            "end",
            iid=str(request["_id"]),
            values=(
                request.get("employee_id", ""),
                request.get("employee_name", ""),
                request.get("leave_type", ""),
                request.get("start_date", ""),
                request.get("end_date", ""),
                request.get("reason", ""),
                request.get("status", "")
            )
        )


def approve_leave():

    selected = leave_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select a leave request."
        )

        return

    request_id = selected[0]

    selected_request = leave_table.item(
        request_id
    )

    values = selected_request["values"]

    current_status = values[6]

    if current_status != "Pending":

        messagebox.showwarning(
            "Already Processed",
            "This leave request has already been processed."
        )

        return

    confirm = messagebox.askyesno(
        "Approve Leave",
        "Are you sure you want to approve this leave request?"
    )

    if not confirm:
        return

    # Update leave status in MongoDB
    update_leave_status(
        request_id,
        "Approved"
    )

    # Refresh leave request table
    load_leave_requests()

    # Refresh dashboard statistics
    refresh_statistics()

    messagebox.showinfo(
        "Success",
        "Leave request approved successfully."
    )


def deny_leave():

    selected = leave_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select a leave request."
        )

        return

    request_id = selected[0]

    selected_request = leave_table.item(
        request_id
    )

    values = selected_request["values"]

    current_status = values[6]

    if current_status != "Pending":

        messagebox.showwarning(
            "Already Processed",
            "This leave request has already been processed."
        )

        return

    confirm = messagebox.askyesno(
        "Deny Leave",
        "Are you sure you want to deny this leave request?"
    )

    if not confirm:
        return

    update_leave_status(
    request_id,
    "Denied"
    )

    load_leave_requests()

    refresh_statistics()

    messagebox.showinfo(
    "Success",
    "Leave request denied."
    )

def record_payment():

    employee_id = payment_employee_combobox.get()
    month = payment_month_entry.get().strip()
    amount = payment_amount_entry.get().strip()
    status = payment_status_combobox.get()

    if not employee_id or not month or not amount or not status:

        messagebox.showwarning(
            "Missing Information",
            "Please fill in all payment information."
        )

        return

    try:
        amount = float(amount)
    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid payment amount."
        )

        return

    # Find employee
    employees = get_all_employees()

    employee = None

    for emp in employees:

        if emp["employee_id"] == employee_id:
            employee = emp
            break

    if employee is None:

        messagebox.showerror(
            "Error",
            "Employee could not be found."
        )

        return

    payment_data = {
        "employee_id": employee["employee_id"],
        "employee_name": employee["name"],
        "month": month,
        "amount": amount,
        "status": status
    }

    create_payment(payment_data)

    messagebox.showinfo(
        "Success",
        "Payment recorded successfully."
    )

    payment_month_entry.delete(0, tk.END)
    payment_amount_entry.delete(0, tk.END)

    payment_status_combobox.current(0)

def refresh_statistics():
    statistics = get_employee_statistics()

    total_value.config(text=str(statistics["total"]))
    active_value.config(text=str(statistics["active"]))
    leave_value.config(text=str(statistics["on_leave"]))
    resigned_value.config(text=str(statistics["resigned"]))

# MAIN WINDOW

root = tk.Tk()

root.title("StaffSync - Admin Dashboard")
root.geometry("1000x750")
root.resizable(True, True)

# TITLE

title_label = tk.Label(
    root,
    text="STAFFSYNC",
    font=("Arial", 26, "bold")
)

title_label.pack(pady=(15, 5))


subtitle_label = tk.Label(
    root,
    text="Admin Dashboard",
    font=("Arial", 16)
)

subtitle_label.pack(pady=5)

# WELCOME

welcome_label = tk.Label(
    root,
    text="Welcome, Admin",
    font=("Arial", 13)
)

welcome_label.pack(pady=5)

# STATISTICS

statistics = get_employee_statistics()

stats_frame = tk.Frame(root)

stats_frame.pack(
    fill="x",
    padx=30,
    pady=15
)


# Total Employees

total_frame = tk.LabelFrame(
    stats_frame,
    text="Total Employees",
    padx=20,
    pady=10
)

total_frame.pack(
    side="left",
    expand=True,
    fill="both",
    padx=5
)

total_value = tk.Label(
    total_frame,
    text=str(statistics["total"]),
    font=("Arial", 22, "bold")
)

total_value.pack()


# Active

active_frame = tk.LabelFrame(
    stats_frame,
    text="Active Employees",
    padx=20,
    pady=10
)

active_frame.pack(
    side="left",
    expand=True,
    fill="both",
    padx=5
)

active_value = tk.Label(
    active_frame,
    text=str(statistics["active"]),
    font=("Arial", 22, "bold")
)
active_value.pack()


# On Leave

leave_frame = tk.LabelFrame(
    stats_frame,
    text="On Leave",
    padx=20,
    pady=10
)

leave_frame.pack(
    side="left",
    expand=True,
    fill="both",
    padx=5
)

leave_value = tk.Label(
    leave_frame,
    text=str(statistics["on_leave"]),
    font=("Arial", 22, "bold")
)

leave_value.pack()

# Resigned

resigned_frame = tk.LabelFrame(
    stats_frame,
    text="Resigned",
    padx=20,
    pady=10
)

resigned_frame.pack(
    side="left",
    expand=True,
    fill="both",
    padx=5
)

resigned_value = tk.Label(
    resigned_frame,
    text=str(statistics["resigned"]),
    font=("Arial", 22, "bold")
)

resigned_value.pack()

# EMPLOYEE MANAGEMENT

management_frame = tk.LabelFrame(
    root,
    text="Employee Management",
    padx=20,
    pady=10
)

management_frame.pack(
    padx=30,
    pady=10,
    fill="x"
)


tk.Label(
    management_frame,
    text="Manage employee records.",
    font=("Arial", 11)
).pack(
    side="left",
    padx=10
)


manage_button = tk.Button(
    management_frame,
    text="Manage Employees",
    width=20,
    command=open_employee_management
)

manage_button.pack(
    side="right",
    padx=10
)

# PAYMENT MANAGEMENT

payment_frame = tk.LabelFrame(
    root,
    text="Payment Management",
    padx=15,
    pady=10
)

payment_frame.pack(
    padx=30,
    pady=10,
    fill="x"
)

# Employee

tk.Label(
    payment_frame,
    text="Employee"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

payment_employee_combobox = ttk.Combobox(
    payment_frame,
    width=20,
    state="readonly"
)

payment_employee_combobox.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

# Month

tk.Label(
    payment_frame,
    text="Month"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5,
    sticky="w"
)

payment_month_entry = tk.Entry(
    payment_frame,
    width=20
)

payment_month_entry.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)

# Amount

tk.Label(
    payment_frame,
    text="Amount"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

payment_amount_entry = tk.Entry(
    payment_frame,
    width=20
)

payment_amount_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

# Status

tk.Label(
    payment_frame,
    text="Status"
).grid(
    row=1,
    column=2,
    padx=5,
    pady=5,
    sticky="w"
)

payment_status_combobox = ttk.Combobox(
    payment_frame,
    values=[
        "Paid",
        "Pending"
    ],
    width=18,
    state="readonly"
)

payment_status_combobox.grid(
    row=1,
    column=3,
    padx=5,
    pady=5
)

payment_status_combobox.current(0)

# Record Payment Button

record_payment_button = tk.Button(
    payment_frame,
    text="Record Payment",
    width=20,
    command=record_payment
)

record_payment_button.grid(
    row=2,
    column=0,
    columnspan=4,
    pady=10
)
# LEAVE REQUESTS

leave_requests_frame = tk.LabelFrame(
    root,
    text="Employee Leave Requests",
    padx=10,
    pady=10
)

leave_requests_frame.pack(
    padx=30,
    pady=10,
    fill="both",
    expand=True
)

# TABLE

columns = (
    "Employee ID",
    "Employee Name",
    "Leave Type",
    "Start Date",
    "End Date",
    "Reason",
    "Status"
)


leave_table = ttk.Treeview(
    leave_requests_frame,
    columns=columns,
    show="headings",
    height=5
)


for column in columns:

    leave_table.heading(
        column,
        text=column
    )

    leave_table.column(
        column,
        width=120
    )


leave_table.column(
    "Reason",
    width=180
)


# Scrollbar

scrollbar = ttk.Scrollbar(
    leave_requests_frame,
    orient="vertical",
    command=leave_table.yview
)

leave_table.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

leave_table.pack(
    fill="both",
    expand=True
)

# LEAVE BUTTONS

leave_button_frame = tk.Frame(
    root
)

leave_button_frame.pack(
    pady=10
)


approve_button = tk.Button(
    leave_button_frame,
    text="Approve Leave",
    width=20,
    command=approve_leave
)

approve_button.grid(
    row=0,
    column=0,
    padx=5
)


deny_button = tk.Button(
    leave_button_frame,
    text="Deny Leave",
    width=20,
    command=deny_leave
)

deny_button.grid(
    row=0,
    column=1,
    padx=5
)


refresh_button = tk.Button(
    leave_button_frame,
    text="Refresh Requests",
    width=20,
    command=load_leave_requests
)

refresh_button.grid(
    row=0,
    column=2,
    padx=5
)

# LOGOUT

logout_button = tk.Button(
    root,
    text="Logout",
    width=20,
    command=logout
)

logout_button.pack(
    pady=5
)

# LOAD LEAVE REQUESTS

load_leave_requests()

load_payment_employees()
# RUN

if __name__ == "__main__":

    root.mainloop()