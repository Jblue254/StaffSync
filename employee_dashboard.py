import tkinter as tk
from tkinter import messagebox

from database import get_employee_by_id


def start_dashboard(employee_id):

    root = tk.Tk()

    root.title("StaffSync - Employee Dashboard")
    root.geometry("700x550")
    root.resizable(False, False)


    # LOGOUT


    def logout():
        root.destroy()

        import login

    # LOAD EMPLOYEE


    employee = get_employee_by_id(employee_id)

    if employee is None:

        messagebox.showerror(
            "Error",
            "Employee information could not be found."
        )

        root.destroy()
        return


    # TITLE
 

    tk.Label(
        root,
        text="STAFFSYNC",
        font=("Arial", 26, "bold")
    ).pack(pady=20)

    # WELCOME


    tk.Label(
        root,
        text=f"Welcome, {employee['name']}",
        font=("Arial", 18)
    ).pack(pady=5)

    tk.Label(
        root,
        text="Employee Dashboard",
        font=("Arial", 12)
    ).pack(pady=5)


    # PROFILE FRAME


    profile_frame = tk.LabelFrame(
        root,
        text="My Profile",
        padx=30,
        pady=20
    )

    profile_frame.pack(
        padx=40,
        pady=20,
        fill="x"
    )

   
    # EMPLOYEE ID

    tk.Label(
        profile_frame,
        text="Employee ID:",
        font=("Arial", 11, "bold")
    ).grid(
        row=0,
        column=0,
        sticky="w",
        pady=8
    )

    tk.Label(
        profile_frame,
        text=employee["employee_id"]
    ).grid(
        row=0,
        column=1,
        sticky="w",
        padx=30,
        pady=8
    )

    # FULL NAME

    tk.Label(
        profile_frame,
        text="Full Name:",
        font=("Arial", 11, "bold")
    ).grid(
        row=1,
        column=0,
        sticky="w",
        pady=8
    )

    tk.Label(
        profile_frame,
        text=employee["name"]
    ).grid(
        row=1,
        column=1,
        sticky="w",
        padx=30,
        pady=8
    )

    # DEPARTMENT

    tk.Label(
        profile_frame,
        text="Department:",
        font=("Arial", 11, "bold")
    ).grid(
        row=2,
        column=0,
        sticky="w",
        pady=8
    )

    tk.Label(profile_frame,text=employee["department"]).grid(row=2,column=1,sticky="w",padx=30,pady=8)

    # SALARY

    tk.Label(profile_frame,text="Salary:",font=("Arial", 11, "bold")).grid(row=3,column=0,sticky="w",pady=8)
    tk.Label(profile_frame,text=employee["salary"]).grid(row=3,column=1,sticky="w",padx=30,pady=8)

    # STATUS

    tk.Label(profile_frame,text="Status:",font=("Arial", 11, "bold")).grid(row=4,column=0,sticky="w",pady=8)
    tk.Label(profile_frame,text=employee["status"]).grid(row=4,column=1,sticky="w",padx=30,pady=8)

    # LOGOUT BUTTON
 
    logout_button = tk.Button(root,text="Logout",width=20,command=logout)
    logout_button.pack(pady=20)

    # RUN

    root.mainloop()