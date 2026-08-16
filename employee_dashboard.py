import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    get_employee_by_id,
    change_password,
    create_leave_request,
    get_employee_leave_requests,
    get_employee_payments

)

COLOR_BG = "#F1F5F9"          # page background
COLOR_CARD = "#FFFFFF"        # card / panel background
COLOR_BORDER = "#CBD5E1"      # card border
COLOR_TEXT = "#0F172A"        # main text
COLOR_MUTED = "#64748B"       # secondary text

COLOR_PRIMARY = "#2563EB"
COLOR_PRIMARY_DARK = "#1E40AF"
COLOR_DANGER = "#DC2626"
COLOR_DANGER_DARK = "#B91C1C"
COLOR_NEUTRAL = "#E2E8F0"
COLOR_NEUTRAL_DARK = "#CBD5E1"

# Fonts unchanged from the original file
FONT_TITLE = ("Arial", 26, "bold")
FONT_WELCOME = ("Arial", 18)
FONT_SUBTITLE = ("Arial", 12)
FONT_DIALOG_TITLE = ("Arial", 18, "bold")
FONT_LEAVE_TITLE = ("Arial", 20, "bold")
FONT_LABEL_BOLD = ("Arial", 11, "bold")


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


def start_dashboard(employee_id, username):

    root = tk.Tk()

    root.title("StaffSync - Employee Dashboard")
    root.resizable(True, True)
    root.configure(bg=COLOR_BG)

    configure_ttk_style()

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
        password_window.configure(bg=COLOR_BG)

        tk.Label(
            password_window,
            text="Change Password",
            font=FONT_DIALOG_TITLE,
            bg=COLOR_BG,
            fg=COLOR_TEXT
        ).pack(pady=20)

        tk.Label(
            password_window,
            text="Current Password",
            bg=COLOR_BG,
            fg=COLOR_TEXT
        ).pack()

        current_password_entry = styled_entry(
            password_window,
            width=30,
            show="*"
        )

        current_password_entry.pack(pady=5)

        tk.Label(
            password_window,
            text="New Password",
            bg=COLOR_BG,
            fg=COLOR_TEXT
        ).pack(pady=(10, 0))

        new_password_entry = styled_entry(
            password_window,
            width=30,
            show="*"
        )

        new_password_entry.pack(pady=5)

        tk.Label(
            password_window,
            text="Confirm New Password",
            bg=COLOR_BG,
            fg=COLOR_TEXT
        ).pack(pady=(10, 0))

        confirm_password_entry = styled_entry(
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

        styled_button(
            password_window,
            text="Change Password",
            command=update_password,
            width=20
        ).pack(pady=20)

    # REQUEST LEAVE

    def open_leave_request():

        leave_window = tk.Toplevel(root)

        leave_window.title("Request Leave")
        leave_window.geometry("450x500")
        leave_window.resizable(False, False)
        leave_window.configure(bg=COLOR_BG)

        tk.Label(
            leave_window,
            text="Request Leave",
            font=FONT_LEAVE_TITLE,
            bg=COLOR_BG,
            fg=COLOR_TEXT
        ).pack(pady=20)

        # Leave Type

        tk.Label(
            leave_window,
            text="Leave Type",
            bg=COLOR_BG,
            fg=COLOR_TEXT
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
            text="Start Date",
            bg=COLOR_BG,
            fg=COLOR_TEXT
        ).pack(pady=(10, 0))

        start_date_entry = styled_entry(
            leave_window,
            width=33
        )

        start_date_entry.pack(pady=5)

        tk.Label(
            leave_window,
            text="Example: 2026-08-20",
            bg=COLOR_BG,
            fg=COLOR_MUTED
        ).pack()

        # End Date

        tk.Label(
            leave_window,
            text="End Date",
            bg=COLOR_BG,
            fg=COLOR_TEXT
        ).pack(pady=(10, 0))

        end_date_entry = styled_entry(
            leave_window,
            width=33
        )

        end_date_entry.pack(pady=5)

        tk.Label(
            leave_window,
            text="Example: 2026-08-25",
            bg=COLOR_BG,
            fg=COLOR_MUTED
        ).pack()

        # Reason

        tk.Label(
            leave_window,
            text="Reason",
            bg=COLOR_BG,
            fg=COLOR_TEXT
        ).pack(pady=(10, 0))

        reason_entry = tk.Text(
            leave_window,
            width=35,
            height=5,
            bg="white",
            fg=COLOR_TEXT,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
            highlightcolor=COLOR_PRIMARY
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

        styled_button(
            leave_window,
            text="Submit Leave Request",
            command=submit_leave,
            width=25
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

    canvas = tk.Canvas(root, bg=COLOR_BG, highlightthickness=0)

    outer_scrollbar = ttk.Scrollbar(
        root,
        orient="vertical",
        command=canvas.yview
    )

    main_frame = tk.Frame(canvas, bg=COLOR_BG)

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
        font=FONT_TITLE,
        bg=COLOR_BG,
        fg=COLOR_TEXT
    ).pack(pady=(15, 5))

    # WELCOME

    tk.Label(
        main_frame,
        text=f"Welcome, {employee['name']}",
        font=FONT_WELCOME,
        bg=COLOR_BG,
        fg=COLOR_TEXT
    ).pack(pady=5)

    tk.Label(
        main_frame,
        text="Employee Dashboard",
        font=FONT_SUBTITLE,
        bg=COLOR_BG,
        fg=COLOR_MUTED
    ).pack(pady=5)

    # PROFILE
 
    profile_frame = styled_labelframe(
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
        font=FONT_LABEL_BOLD,
        bg=COLOR_CARD,
        fg=COLOR_TEXT
    ).grid(
        row=0,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Label(
        profile_frame,
        text=employee["employee_id"],
        bg=COLOR_CARD,
        fg=COLOR_TEXT
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
        font=FONT_LABEL_BOLD,
        bg=COLOR_CARD,
        fg=COLOR_TEXT
    ).grid(
        row=1,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Label(
        profile_frame,
        text=employee["name"],
        bg=COLOR_CARD,
        fg=COLOR_TEXT
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
        font=FONT_LABEL_BOLD,
        bg=COLOR_CARD,
        fg=COLOR_TEXT
    ).grid(
        row=2,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Label(
        profile_frame,
        text=employee["department"],
        bg=COLOR_CARD,
        fg=COLOR_TEXT
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
        font=FONT_LABEL_BOLD,
        bg=COLOR_CARD,
        fg=COLOR_TEXT
    ).grid(
        row=3,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Label(
        profile_frame,
        text=employee["salary"],
        bg=COLOR_CARD,
        fg=COLOR_TEXT
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
        font=FONT_LABEL_BOLD,
        bg=COLOR_CARD,
        fg=COLOR_TEXT
    ).grid(
        row=4,
        column=0,
        sticky="w",
        pady=5
    )

    tk.Label(
        profile_frame,
        text=employee["status"],
        bg=COLOR_CARD,
        fg=COLOR_TEXT
    ).grid(
        row=4,
        column=1,
        sticky="w",
        padx=30,
        pady=5
    )

    # BUTTONS

    button_frame = tk.Frame(main_frame, bg=COLOR_BG)

    button_frame.pack(pady=6)

    change_password_button = styled_button(
        button_frame,
        text="Change Password",
        command=open_change_password,
        bg=COLOR_NEUTRAL,
        active_bg=COLOR_NEUTRAL_DARK,
        width=20
    )

    change_password_button.config(fg=COLOR_TEXT, activeforeground=COLOR_TEXT)

    change_password_button.grid(
        row=0,
        column=0,
        padx=5
    )

    leave_button = styled_button(
        button_frame,
        text="Request Leave",
        command=open_leave_request,
        bg=COLOR_PRIMARY,
        active_bg=COLOR_PRIMARY_DARK,
        width=20
    )

    leave_button.grid(
        row=0,
        column=1,
        padx=5
    )

    logout_button = styled_button(
        button_frame,
        text="Logout",
        command=logout,
        bg=COLOR_DANGER,
        active_bg=COLOR_DANGER_DARK,
        width=20
    )

    logout_button.grid(
        row=0,
        column=2,
        padx=5
    )

    # LEAVE REQUESTS

    leave_frame = styled_labelframe(
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

    payment_frame = styled_labelframe(
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