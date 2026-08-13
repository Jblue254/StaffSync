import tkinter as tk
from tkinter import messagebox

from database import get_employee_by_id


def start_dashboard(employee_id):

    root = tk.Tk()

    root.title("StaffSync - Employee Dashboard")
    root.geometry("700x500")
    root.resizable(False, False)

    def load_employee():

        employee = get_employee_by_id(employee_id)

        if employee is None:

            messagebox.showerror(
                "Error",
                "Employee information could not be found."
            )

            return

        id_value.config(text=employee["employee_id"])
        name_value.config(text=employee["name"])
        department_value.config(text=employee["department"])
        salary_value.config(text=employee["salary"])
        status_value.config(text=employee["status"])

    # TITLE
   
    tk.Label(root,text="STAFFSYNC",font=("Arial", 26, "bold")).pack(pady=20)
    tk.Label(root,text="Employee Dashboard",font=("Arial", 18)).pack(pady=10)

    # INFORMATION
    info_frame = tk.LabelFrame(root,text="My Information",padx=30,pady=20)
    info_frame.pack(pady=20)

    # Employee ID

    tk.Label(info_frame,text="Employee ID:").grid(row=0,column=0,sticky="w",pady=8)
    id_value = tk.Label(info_frame,text="-",width=25,anchor="w")
    id_value.grid(row=0,column=1,pady=8)

    # Name

    tk.Label(info_frame,text="Full Name:").grid(row=1,column=0,sticky="w",pady=8)
    name_value = tk.Label(info_frame,text="-",width=25,anchor="w")
    name_value.grid(row=1,column=1,pady=8)

    # Department

    tk.Label(info_frame,text="Department:").grid(row=2,column=0,sticky="w",pady=8)
    department_value = tk.Label(info_frame,text="-",width=25,anchor="w")
    department_value.grid(row=2,column=1,pady=8)

    # Salary

    tk.Label(info_frame,text="Salary:").grid(row=3,column=0,sticky="w",pady=8)
    salary_value = tk.Label(info_frame,text="-",width=25,anchor="w")
    salary_value.grid(row=3,column=1,pady=8)

    # Status

    tk.Label(info_frame,text="Status:").grid(row=4,column=0,sticky="w",pady=8)
    status_value = tk.Label(info_frame,text="-",width=25,anchor="w")
    status_value.grid(row=4,column=1,pady=8)

    # Logout

    tk.Button(root,text="Logout",width=20,command=root.destroy).pack(pady=10)

    load_employee()

    root.mainloop()