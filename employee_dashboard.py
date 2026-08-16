import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    get_employee_by_id,
    change_password,
    create_leave_request,
    get_employee_leave_requests,
    get_employee_payments

)

def start_dashboard(employee_id, username):

    root = tk.Tk()

    root.title("StaffSync - Employee Dashboard")
    root.resizable(True, True)

    try:
        root.state("zoomed")
    except tk.TclError:
        root.attributes("-zoomed", True)

    # LOGOUT

    def logout():

        root.destroy()

        import login

    # CHANGE PASSWORD

    def open_change_password():

        password_window = tk.Toplevel(root)

        password_window.title("Change Password")
        password_window.geometry("400x350")
        password_window.resizable(False, False)

        tk.Label(
            password_window,
            text="Change Password",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(
            password_window,
            text="Current Password"
        ).pack()

        current_password_entry = tk.Entry(
            password_window,
            width=30,
            show="*"
        )

        current_password_entry.pack(pady=5)

        tk.Label(
            password_window,
            text="New Password"
        ).pack(pady=(10, 0))

        new_password_entry = tk.Entry(
            password_window,
            width=30,
            show="*"
        )

        new_password_entry.pack(pady=5)

        tk.Label(
            password_window,
            text="Confirm New Password"
        ).pack(pady=(10, 0))

        confirm_password_entry = tk.Entry(
            password_window,
            width=30,
            show="*"
        )

        confirm_password_entry.pack(pady=5)

        def update_password():

            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            if not current_password or not new_password or not confirm_password:

                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all fields."
                )

                return

            if new_password != confirm_password:

                messagebox.showerror(
                    "Password Error",
                    "New passwords do not match."
                )

                return

            if current_password == new_password:

                messagebox.showwarning(
                    "Password Error",
                    "New password must be different from the current password."
                )

                return

            success = change_password(
                username,
                current_password,
                new_password
            )

            if not success:

                messagebox.showerror(
                    "Password Error",
                    "Current password is incorrect."
                )

                return

            messagebox.showinfo(
                "Success",
                "Password changed successfully."
            )

            password_window.destroy()

        tk.Button(
            password_window,
            text="Change Password",
            width=20,
            command=update_password
        ).pack(pady=20)

    # REQUEST LEAVE

    def open_leave_request():

        leave_window = tk.Toplevel(root)

        leave_window.title("Request Leave")
        leave_window.geometry("450x500")
        leave_window.resizable(False, False)

        tk.Label(
            leave_window,
            text="Request Leave",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # Leave Type

        tk.Label(
            leave_window,
            text="Leave Type"
        ).pack()

        leave_type_combobox = ttk.Combobox(
            leave_window,
            values=[
                "Annual Leave",
                "Sick Leave",
                "Maternity Leave",
                "Paternity Leave",
                "Emergency Leave",
                "Unpaid Leave"
            ],
            width=30,
            state="readonly"
        )

        leave_type_combobox.pack(pady=5)

        leave_type_combobox.current(0)

        # Start Date

        tk.Label(
            leave_window,
            text="Start Date"
        ).pack(pady=(10, 0))

        start_date_entry = tk.Entry(
            leave_window,
            width=33
        )

        start_date_entry.pack(pady=5)

        tk.Label(
            leave_window,
            text="Example: 2026-08-20"
        ).pack()

        # End Date

        tk.Label(
            leave_window,
            text="End Date"
        ).pack(pady=(10, 0))

        end_date_entry = tk.Entry(
            leave_window,
            width=33
        )

        end_date_entry.pack(pady=5)

        tk.Label(
            leave_window,
            text="Example: 2026-08-25"
        ).pack()

        # Reason

        tk.Label(
            leave_window,
            text="Reason"
        ).pack(pady=(10, 0))

        reason_entry = tk.Text(
            leave_window,
            width=35,
            height=5
        )

        reason_entry.pack(pady=5)

        # Submit

        def submit_leave():

            leave_type = leave_type_combobox.get()
            start_date = start_date_entry.get().strip()
            end_date = end_date_entry.get().strip()
            reason = reason_entry.get("1.0", tk.END).strip()

            if not leave_type or not start_date or not end_date or not reason:

                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all fields."
                )

                return

            leave_data = {

                "employee_id": employee_id,

                "employee_name": employee["name"],

                "leave_type": leave_type,

                "start_date": start_date,

                "end_date": end_date,

                "reason": reason,

                "status": "Pending"
            }

            create_leave_request(leave_data)

            messagebox.showinfo(
                "Success",
                "Your leave request has been submitted.\n\n"
                "Status: Pending"
            )

            leave_window.destroy()

            load_leave_requests()

        tk.Button(
            leave_window,
            text="Submit Leave Request",
            width=25,
            command=submit_leave
        ).pack(pady=20)

 
    # LOAD LEAVE REQUESTS


    def load_leave_requests():

        for item in leave_table.get_children():

            leave_table.delete(item)

        requests = get_employee_leave_requests(employee_id)

        for request in requests:

            leave_table.insert(
                "",
                "end",
                values=(
                    request.get("leave_type", ""),
                    request.get("start_date", ""),
                    request.get("end_date", ""),
                    request.get("reason", ""),
                    request.get("status", "")
                )
            )
    def load_payments():

        for item in payment_table.get_children():
            payment_table.delete(item)

        payments = get_employee_payments(employee_id)

        for payment in payments:

            payment_table.insert(
                "",
                "end",
                values=(
                    payment.get("month", ""),
                    payment.get("amount", ""),
                    payment.get("status", "")
                )
            )
    # GET EMPLOYEE

    employee = get_employee_by_id(employee_id)

    if employee is None:

        messagebox.showerror(
            "Error",
            "Employee information could not be found."
        )

        root.destroy()

        return

    # SCROLLABLE CONTAINER
    # (root has a fixed size, so without this, content below the
    # visible area - like the payment table - never shows up)

    canvas = tk.Canvas(root, highlightthickness=0)

    outer_scrollbar = ttk.Scrollbar(
        root,
        orient="vertical",
        command=canvas.yview
    )

    main_frame = tk.Frame(canvas)

    main_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    main_frame_window = canvas.create_window(
        (0, 0),
        window=main_frame,
        anchor="nw"
    )

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfig(main_frame_window, width=e.width)
    )

    canvas.configure(yscrollcommand=outer_scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)

    outer_scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # TITLE

    tk.Label(
        main_frame,
        text="STAFFSYNC",
        font=("Arial", 26, "bold")
    ).pack(pady=(15, 5))

    # WELCOME

    tk.Label(
        main_frame,
        text=f"Welcome, {employee['name']}",
        font=("Arial", 18)
    ).pack(pady=5)

    tk.Label(
        main_frame,
        text="Employee Dashboard",
        font=("Arial", 12)
    ).pack(pady=5)

    # PROFILE
 
    profile_frame = tk.LabelFrame(
        main_frame,
        text="My Profile",
        padx=30,
        pady=15
    )

    profile_frame.pack(
        padx=40,
        pady=8,
        fill="x"
    )

    # Employee ID

    tk.Label(
        profile_frame,
        text="Employee ID:",
        font=("Arial", 11, "bold")
    ).grid(
        row=0,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Label(
        profile_frame,
        text=employee["employee_id"]
    ).grid(
        row=0,
        column=1,
        sticky="w",
        padx=30,
        pady=5
    )

    # Full Name

    tk.Label(
        profile_frame,
        text="Full Name:",
        font=("Arial", 11, "bold")
    ).grid(
        row=1,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Label(
        profile_frame,
        text=employee["name"]
    ).grid(
        row=1,
        column=1,
        sticky="w",
        padx=30,
        pady=5
    )

    # Department

    tk.Label(
        profile_frame,
        text="Department:",
        font=("Arial", 11, "bold")
    ).grid(
        row=2,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Label(
        profile_frame,
        text=employee["department"]
    ).grid(
        row=2,
        column=1,
        sticky="w",
        padx=30,
        pady=5
    )

    # Salary

    tk.Label(
        profile_frame,
        text="Salary:",
        font=("Arial", 11, "bold")
    ).grid(
        row=3,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Label(
        profile_frame,
        text=employee["salary"]
    ).grid(
        row=3,
        column=1,
        sticky="w",
        padx=30,
        pady=5
    )

    # Status

    tk.Label(
        profile_frame,
        text="Status:",
        font=("Arial", 11, "bold")
    ).grid(
        row=4,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Label(
        profile_frame,
        text=employee["status"]
    ).grid(
        row=4,
        column=1,
        sticky="w",
        padx=30,
        pady=5
    )

    # BUTTONS

    button_frame = tk.Frame(main_frame)

    button_frame.pack(pady=6)

    change_password_button = tk.Button(
        button_frame,
        text="Change Password",
        width=20,
        command=open_change_password
    )

    change_password_button.grid(
        row=0,
        column=0,
        padx=5
    )

    leave_button = tk.Button(
        button_frame,
        text="Request Leave",
        width=20,
        command=open_leave_request
    )

    leave_button.grid(
        row=0,
        column=1,
        padx=5
    )

    logout_button = tk.Button(
        button_frame,
        text="Logout",
        width=20,
        command=logout
    )

    logout_button.grid(
        row=0,
        column=2,
        padx=5
    )

    # LEAVE REQUESTS

    leave_frame = tk.LabelFrame(
        main_frame,
        text="My Leave Requests",
        padx=10,
        pady=10
    )

    leave_frame.pack(
        padx=40,
        pady=10,
        fill="both"
    )

    columns = (
        "Leave Type",
        "Start Date",
        "End Date",
        "Reason",
        "Status"
    )

    leave_table = ttk.Treeview(
        leave_frame,
        columns=columns,
        show="headings",
        height=4
    )

    for column in columns:

        leave_table.heading(
            column,
            text=column
        )

        leave_table.column(
            column,
            width=130
        )

    scrollbar = ttk.Scrollbar(
        leave_frame,
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
    
    # PAYMENT / SALARY

    payment_frame = tk.LabelFrame(
        main_frame,
        text="My Payments / Salary",
        padx=10,
        pady=10
    )

    payment_frame.pack(
        padx=40,
        pady=10,
        fill="both"
    )

    payment_columns = (
        "Month",
        "Amount",
        "Status"
    )

    payment_table = ttk.Treeview(
        payment_frame,
        columns=payment_columns,
        show="headings",
        height=3
    )

    for column in payment_columns:

        payment_table.heading(
            column,
            text=column
        )

        payment_table.column(
            column,
            width=150
        )

    payment_scrollbar = ttk.Scrollbar(
        payment_frame,
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

    

    # LOAD LEAVE REQUESTS

    load_leave_requests()

    # LOAD PAYMENTS

    load_payments()

    # RUN

    root.mainloop()