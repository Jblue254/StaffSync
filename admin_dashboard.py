import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    get_employee_statistics,
    get_all_leave_requests,
    update_leave_status,
    get_all_employees,
    create_payment,
    get_all_payments
)

# -----------------------------------------------------------------
# STYLE CONSTANTS
# -----------------------------------------------------------------

COLOR_BG = "#F1F5F9"          # page background
COLOR_CARD = "#FFFFFF"        # card / panel background
COLOR_BORDER = "#CBD5E1"      # card border
COLOR_TEXT = "#0F172A"        # main text
COLOR_MUTED = "#64748B"       # secondary text

COLOR_PRIMARY = "#2563EB"
COLOR_PRIMARY_DARK = "#1E40AF"
COLOR_SUCCESS = "#16A34A"
COLOR_SUCCESS_DARK = "#15803D"
COLOR_DANGER = "#DC2626"
COLOR_DANGER_DARK = "#B91C1C"
COLOR_NEUTRAL = "#E2E8F0"
COLOR_NEUTRAL_DARK = "#CBD5E1"

# Fonts unchanged from the original file
FONT_TITLE = ("Arial", 26, "bold")
FONT_SUBTITLE = ("Arial", 16)
FONT_WELCOME = ("Arial", 13)
FONT_STAT_VALUE = ("Arial", 22, "bold")


def styled_button(parent, text, command, bg=COLOR_PRIMARY, active_bg=COLOR_PRIMARY_DARK, width=20):

    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        bg=bg,
        fg="white",
        activebackground=active_bg,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=8,
        pady=6
    )


def styled_labelframe(parent, text, **kwargs):

    return tk.LabelFrame(
        parent,
        text=text,
        bg=COLOR_CARD,
        fg=COLOR_TEXT,
        bd=1,
        relief="solid",
        highlightbackground=COLOR_BORDER,
        **kwargs
    )


def styled_entry(parent, **kwargs):

    return tk.Entry(
        parent,
        bg="white",
        fg=COLOR_TEXT,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=COLOR_BORDER,
        highlightcolor=COLOR_PRIMARY,
        **kwargs
    )


def configure_ttk_style():

    style = ttk.Style()

    style.theme_use("clam")

    # Treeview

    style.configure(
        "Treeview",
        background=COLOR_CARD,
        fieldbackground=COLOR_CARD,
        foreground=COLOR_TEXT,
        rowheight=28,
        borderwidth=0
    )

    style.configure(
        "Treeview.Heading",
        background=COLOR_PRIMARY,
        foreground="white",
        relief="flat"
    )

    style.map(
        "Treeview.Heading",
        background=[("active", COLOR_PRIMARY_DARK)]
    )

    style.map(
        "Treeview",
        background=[("selected", COLOR_PRIMARY)],
        foreground=[("selected", "white")]
    )

    # Combobox

    style.configure(
        "TCombobox",
        fieldbackground="white",
        background="white",
        foreground=COLOR_TEXT,
        arrowcolor=COLOR_PRIMARY,
        bordercolor=COLOR_BORDER,
        padding=4
    )

    style.map(
        "TCombobox",
        fieldbackground=[("readonly", "white")],
        foreground=[("readonly", COLOR_TEXT)]
    )

    # Scrollbar

    style.configure(
        "Vertical.TScrollbar",
        background=COLOR_NEUTRAL,
        troughcolor=COLOR_BG,
        bordercolor=COLOR_BG,
        arrowcolor=COLOR_MUTED,
        relief="flat"
    )


# FUNCTIONS

def fill_employee_salary(event=None):

    employee_id = payment_employee_combobox.get()

    if not employee_id:
        return

    employees = get_all_employees()

    for employee in employees:

        if employee["employee_id"] == employee_id:

            payment_amount_entry.delete(0, tk.END)

            payment_amount_entry.insert(
                0,
                employee["salary"]
            )

            break


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
        fill_employee_salary()

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

    load_payments()

    messagebox.showinfo(
        "Success",
        "Payment recorded successfully."
    )

    payment_month_entry.delete(0, tk.END)
    payment_amount_entry.delete(0, tk.END)

    payment_status_combobox.current(0)

def load_payments():

    payment_table.delete(
        *payment_table.get_children()
    )

    payments = get_all_payments()

    for payment in payments:

        payment_table.insert(
            "",
            "end",
            values=(
                payment.get("employee_id", ""),
                payment.get("employee_name", ""),
                payment.get("month", ""),
                payment.get("amount", ""),
                payment.get("status", "")
            )
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
root.configure(bg=COLOR_BG)

configure_ttk_style()

# TITLE

title_label = tk.Label(
    root,
    text="STAFFSYNC",
    font=FONT_TITLE,
    bg=COLOR_BG,
    fg=COLOR_TEXT
)

title_label.pack(pady=(15, 5))


subtitle_label = tk.Label(
    root,
    text="Admin Dashboard",
    font=FONT_SUBTITLE,
    bg=COLOR_BG,
    fg=COLOR_MUTED
)

subtitle_label.pack(pady=5)

# WELCOME

welcome_label = tk.Label(
    root,
    text="Welcome, Admin",
    font=FONT_WELCOME,
    bg=COLOR_BG,
    fg=COLOR_MUTED
)

welcome_label.pack(pady=5)

# STATISTICS

statistics = get_employee_statistics()

stats_frame = tk.Frame(root, bg=COLOR_BG)

stats_frame.pack(
    fill="x",
    padx=30,
    pady=15
)


# Total Employees

total_frame = styled_labelframe(
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
    font=FONT_STAT_VALUE,
    bg=COLOR_CARD,
    fg=COLOR_PRIMARY
)

total_value.pack()

# Active

active_frame = styled_labelframe(
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
    font=FONT_STAT_VALUE,
    bg=COLOR_CARD,
    fg=COLOR_SUCCESS
)
active_value.pack()


# On Leave

leave_frame = styled_labelframe(
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
    font=FONT_STAT_VALUE,
    bg=COLOR_CARD,
    fg="#D97706"
)

leave_value.pack()

# Resigned

resigned_frame = styled_labelframe(
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
    font=FONT_STAT_VALUE,
    bg=COLOR_CARD,
    fg=COLOR_DANGER
)

resigned_value.pack()

# EMPLOYEE MANAGEMENT

management_frame = styled_labelframe(
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
    bg=COLOR_CARD,
    fg=COLOR_TEXT
).pack(
    side="left",
    padx=10
)


manage_button = styled_button(
    management_frame,
    text="Manage Employees",
    command=open_employee_management,
    bg=COLOR_PRIMARY,
    active_bg=COLOR_PRIMARY_DARK
)

manage_button.pack(
    side="right",
    padx=10
)

# PAYMENT MANAGEMENT

payment_frame = styled_labelframe(
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
    text="Employee",
    bg=COLOR_CARD,
    fg=COLOR_TEXT
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
    state="readonly",
)

payment_employee_combobox.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

payment_employee_combobox.bind(
    "<<ComboboxSelected>>",
    fill_employee_salary
)

# Month

tk.Label(
    payment_frame,
    text="Month",
    bg=COLOR_CARD,
    fg=COLOR_TEXT
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5,
    sticky="w"
)

payment_month_entry = styled_entry(
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
    text="Amount",
    bg=COLOR_CARD,
    fg=COLOR_TEXT
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

payment_amount_entry = styled_entry(
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
    text="Status",
    bg=COLOR_CARD,
    fg=COLOR_TEXT
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
    state="readonly",
)

payment_status_combobox.grid(
    row=1,
    column=3,
    padx=5,
    pady=5
)

payment_status_combobox.current(0)

# Record Payment Button

record_payment_button = styled_button(
    payment_frame,
    text="Record Payment",
    command=record_payment,
    bg=COLOR_PRIMARY,
    active_bg=COLOR_PRIMARY_DARK
)

record_payment_button.grid(
    row=2,
    column=0,
    columnspan=4,
    pady=10
)

# PAYMENT HISTORY

payment_history_frame = styled_labelframe(
    root,
    text="Payment History",
    padx=10,
    pady=10
)

payment_history_frame.pack(
    padx=30,
    pady=10,
    fill="both",
    expand=True
)

# TABLE COLUMNS

payment_columns = (
    "Employee ID",
    "Employee Name",
    "Month",
    "Amount",
    "Status"
)

payment_table = ttk.Treeview(
    payment_history_frame,
    columns=payment_columns,
    show="headings",
    height=5
)

for column in payment_columns:

    payment_table.heading(
        column,
        text=column
    )

    payment_table.column(
        column,
        width=140
    )

# Scrollbar

payment_scrollbar = ttk.Scrollbar(
    payment_history_frame,
    orient="vertical",
    command=payment_table.yview
)

payment_table.configure(
    yscrollcommand=payment_scrollbar.set
)

payment_scrollbar.pack(
    side="right",
    fill="y"
)

payment_table.pack(
    fill="both",
    expand=True
)

# Refresh Payments Button

refresh_payments_button = styled_button(
    payment_history_frame,
    text="Refresh Payments",
    command=load_payments,
    bg=COLOR_NEUTRAL,
    active_bg=COLOR_NEUTRAL_DARK
)

refresh_payments_button.config(fg=COLOR_TEXT, activeforeground=COLOR_TEXT)

refresh_payments_button.pack(
    pady=5
)

# LEAVE REQUESTS

leave_requests_frame = styled_labelframe(
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
    root,
    bg=COLOR_BG
)

leave_button_frame.pack(
    pady=10
)


approve_button = styled_button(
    leave_button_frame,
    text="Approve Leave",
    command=approve_leave,
    bg=COLOR_SUCCESS,
    active_bg=COLOR_SUCCESS_DARK
)

approve_button.grid(
    row=0,
    column=0,
    padx=5
)


deny_button = styled_button(
    leave_button_frame,
    text="Deny Leave",
    command=deny_leave,
    bg=COLOR_DANGER,
    active_bg=COLOR_DANGER_DARK
)

deny_button.grid(
    row=0,
    column=1,
    padx=5
)


refresh_button = styled_button(
    leave_button_frame,
    text="Refresh Requests",
    command=load_leave_requests,
    bg=COLOR_NEUTRAL,
    active_bg=COLOR_NEUTRAL_DARK
)

refresh_button.config(fg=COLOR_TEXT, activeforeground=COLOR_TEXT)

refresh_button.grid(
    row=0,
    column=2,
    padx=5
)

# LOGOUT

logout_button = styled_button(
    root,
    text="Logout",
    command=logout,
    bg=COLOR_DANGER,
    active_bg=COLOR_DANGER_DARK
)

logout_button.pack(
    pady=5
)

load_leave_requests()

load_payment_employees()

load_payments()
# RUN

if __name__ == "__main__":

    root.mainloop()