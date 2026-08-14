import tkinter as tk

from database import get_employee_statistics
from department_management import open_department_management

def open_employee_management():

    root.destroy()

    import app


def logout():

    root.destroy()

    import login


# MAIN WINDOW


root = tk.Tk()

root.title("StaffSync - Admin Dashboard")
root.state("zoomed")
root.resizable(False, False)


# TITLE


title_label = tk.Label(
    root,
    text="STAFFSYNC",
    font=("Arial", 26, "bold")
)

title_label.pack(pady=(20, 5))


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

welcome_label.pack(pady=10)


# STATISTICS

statistics = get_employee_statistics()

stats_frame = tk.Frame(root)

stats_frame.pack(
    fill="x",
    padx=40,
    pady=20
)

# TOTAL EMPLOYEES

total_frame = tk.LabelFrame(
    stats_frame,
    text="Total Employees",
    padx=20,
    pady=15
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
    font=("Arial", 24, "bold")
)

total_value.pack()

# ACTIVE EMPLOYEES

active_frame = tk.LabelFrame(
    stats_frame,
    text="Active Employees",
    padx=20,
    pady=15
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
    font=("Arial", 24, "bold")
)

active_value.pack()


# ON LEAVE

leave_frame = tk.LabelFrame(
    stats_frame,
    text="On Leave",
    padx=20,
    pady=15
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
    font=("Arial", 24, "bold")
)

leave_value.pack()

# RESIGNED

resigned_frame = tk.LabelFrame(
    stats_frame,
    text="Resigned",
    padx=20,
    pady=15
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
    font=("Arial", 24, "bold")
)

resigned_value.pack()


# EMPLOYEE MANAGEMENT

management_frame = tk.LabelFrame(
    root,
    text="Employee Management",
    padx=30,
    pady=30
)

management_frame.pack(
    padx=40,
    pady=30,
    fill="x"
)


tk.Label(
    management_frame,
    text="Add, update, delete and manage employee records.",
    font=("Arial", 12)
).pack(pady=10)


manage_button = tk.Button(
    management_frame,
    text="Manage Employees",
    width=30,
    height=2,
    command=open_employee_management
)

manage_button.pack(pady=10)
# =========================
# DEPARTMENT MANAGEMENT
# =========================

department_frame = tk.LabelFrame(
    root,
    text="Department Management",
    padx=30,
    pady=20
)

department_frame.pack(
    padx=40,
    pady=10,
    fill="x"
)


tk.Label(
    department_frame,
    text="Add and manage company departments.",
    font=("Arial", 12)
).pack(pady=5)


department_button = tk.Button(
    department_frame,
    text="Manage Departments",
    width=30,
    height=2,
    command=open_department_management
)

department_button.pack(pady=5)

# LOGOUT

logout_button = tk.Button(
    root,
    text="Logout",
    width=20,
    command=logout
)

logout_button.pack(pady=10)

# RUN

if __name__ == "__main__":
    root.mainloop()