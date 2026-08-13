import tkinter as tk
from tkinter import messagebox

from database import login_user


def open_dashboard(user):

    role = user["role"]

    root.destroy()

    if role == "admin":

        import admin_dashboard

    elif role == "employee":

        import employee_dashboard

        employee_dashboard.start_dashboard(
            user["employee_id"]
        )


def login():

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        
        messagebox.showwarning("Missing Information","Please enter username and password.")

        return

    user = login_user(username,password)

    if user is None:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )
        return

    open_dashboard(user)


# LOGIN WINDOW

root = tk.Tk()

root.title("StaffSync Login")
root.geometry("400x300")
root.resizable(False, False)


# TITLE

tk.Label(root,text="STAFFSYNC",font=("Arial", 22, "bold")).pack(pady=20)

# USERNAME

tk.Label(root,text="Username").pack()
username_entry = tk.Entry(root,width=30)
username_entry.pack(pady=5)

# PASSWORD

tk.Label(root,text="Password").pack()
password_entry = tk.Entry(root,width=30,show="*")
password_entry.pack(pady=5)

# LOGIN BUTTON

tk.Button(root,text="Login",width=20,command=login).pack(pady=20)

# RUN

root.mainloop()