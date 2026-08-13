import tkinter as tk


def open_employee_management():

    # Open the employee management system
    import app


def logout():

    root.destroy()

# ADMIN DASHBOARD

root = tk.Tk()

root.title("StaffSync - Admin Dashboard")
root.geometry("700x500")
root.resizable(False, False)


# TITLE


title_label = tk.Label(root,text="ADMIN DASHBOARD",font=("Arial", 26, "bold"))
title_label.pack(pady=20)


# WELCOME MESSAGE

welcome_label = tk.Label(root,text="Welcome, Admini",font=("Arial", 18))
welcome_label.pack(pady=10)


# DESCRIPTION

description_label = tk.Label(root,text="Manage employees and view employee information.",font=("Arial", 12))
description_label.pack(pady=10)

# EMPLOYEE MANAGEMENT

employee_button = tk.Button(root,text="Employee Management",width=30,height=2,command=open_employee_management)
employee_button.pack(pady=20)

# LOGOUT

logout_button = tk.Button(root,text="Logout",width=20,command=logout)
logout_button.pack(pady=10)

# RUN

root.mainloop()