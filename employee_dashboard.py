import tkinter as tk
from tkinter import messagebox

from database import (get_employee_by_id,change_password)


def start_dashboard(employee_id, username):

    root = tk.Tk()

    root.title("StaffSync - Employee Dashboard")
    root.geometry("700x550")
    root.resizable(False, False)

    # LOGOUT

    def logout():
        root.destroy()

        import login
    
def open_change_password():

    password_window = tk.Toplevel(root)

    password_window.title("Change Password")
    password_window.geometry("400x350")
    password_window.resizable(False, False)

    # TITLE


    tk.Label(
        password_window,
        text="Change Password",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    # CURRENT PASSWORD


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

    # NEW PASSWORD


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

  
    # CONFIRM PASSWORD
  

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

  
    # UPDATE PASSWORD


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

 
    # BUTTON


    tk.Button(
        password_window,
        text="Change Password",
        width=20,
        command=update_password
    ).pack(pady=20)

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
     
    #CHANGE PASSWORD BUTTON
    change_password_button = tk.Button(root,text="Change Password",width=20,command=open_change_password)
    change_password_button.pack(pady=5)
    
    # LOGOUT BUTTON
 
    logout_button = tk.Button(root,text="Logout",width=20,command=logout)
    logout_button.pack(pady=20)



    # RUN

    root.mainloop()