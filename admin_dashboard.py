import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    get_employee_statistics,
    get_all_leave_requests,
    update_leave_status
)

# FUNCTIONS

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

# RUN

if __name__ == "__main__":

    root.mainloop()