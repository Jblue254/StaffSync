import tkinter as tk
from tkinter import messagebox

from database import (
    add_department,
    get_all_departments,
    delete_department
)


def open_department_management():

    root = tk.Toplevel()

    root.title("StaffSync - Department Management")
    root.geometry("600x500")
    root.resizable(False, False)

    # TITLE

    tk.Label(
        root,
        text="DEPARTMENT MANAGEMENT",
        font=("Arial", 20, "bold")
    ).pack(pady=20)


    # ADD DEPARTMENT


    tk.Label(
        root,
        text="Department Name"
    ).pack()

    department_entry = tk.Entry(
        root,
        width=35
    )

    department_entry.pack(pady=5)


    # DEPARTMENT LIST
  

    department_list = tk.Listbox(
        root,
        width=50,
        height=12
    )

    department_list.pack(pady=20)

  
    # LOAD DEPARTMENTS
    

    def load_departments():

        department_list.delete(
            0,
            tk.END
        )

        departments = get_all_departments()

        for department in departments:

            department_list.insert(
                tk.END,
                department["name"]
            )

    # ADD
  

    def add_new_department():

        department_name = department_entry.get().strip()

        if not department_name:

            messagebox.showwarning(
                "Missing Information",
                "Please enter a department name."
            )

            return

        existing_departments = get_all_departments()

        for department in existing_departments:

            if department["name"].lower() == department_name.lower():

                messagebox.showwarning(
                    "Duplicate Department",
                    "This department already exists."
                )

                return

        add_department({
            "name": department_name
        })

        department_entry.delete(
            0,
            tk.END
        )

        load_departments()

        messagebox.showinfo(
            "Success",
            "Department added successfully."
        )

 
    # DELETE


    def remove_department():

        selected = department_list.curselection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a department."
            )

            return

        department_name = department_list.get(
            selected[0]
        )

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {department_name}?"
        )

        if not confirm:
            return

        delete_department(
            department_name
        )

        load_departments()

        messagebox.showinfo(
            "Success",
            "Department deleted successfully."
        )


    # BUTTONS


    tk.Button(
        root,
        text="Add Department",
        width=25,
        command=add_new_department
    ).pack(pady=5)

    tk.Button(
        root,
        text="Delete Department",
        width=25,
        command=remove_department
    ).pack(pady=5)

 
    # LOAD

    load_departments()