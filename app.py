import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    add_employee as save_employee,
    get_all_employees,
    get_all_departments,
    generate_employee_id,
    create_user,
    update_employee as update_employee_database,
    delete_employee as delete_employee_database,
    search_employees
)

# -----------------------------------------------------------------
# STYLE CONSTANTS (same palette as the admin dashboard)
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
FONT_TITLE = ("Arial", 20, "bold")


def styled_button(parent, text, command, bg=COLOR_PRIMARY, active_bg=COLOR_PRIMARY_DARK, width=25):

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

def select_employee(event):

    selected = employee_table.selection()

    if not selected:
        return

    employee = employee_table.item(selected[0])

    values = employee["values"]

    name_entry.delete(0, tk.END)
    name_entry.insert(0, values[1])

    department_combobox.set(values[2])

    salary_entry.delete(0, tk.END)
    salary_entry.insert(0, values[3])

    status_combobox.set(values[4])


def add_employee():

    name = name_entry.get().strip()
    department = department_combobox.get()
    salary = salary_entry.get().strip()
    status = status_combobox.get()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not name or not department or not salary or not username or not password:

        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )

        return

    employee_id = generate_employee_id()

    employee_data = {
        "employee_id": employee_id,
        "name": name,
        "department": department,
        "salary": salary,
        "status": status
    }

    user_data = {
        "username": username,
        "password": password,
        "role": "employee",
        "employee_id": employee_id
    }

    save_employee(employee_data)

    create_user(user_data)

    load_employees()

    clear_fields()

    messagebox.showinfo(
        "Success",
        f"Employee added successfully!\n\nEmployee ID: {employee_id}"
    )


def search_employee():

    keyword = search_entry.get().strip()

    employee_table.delete(
        *employee_table.get_children()
    )

    employees = search_employees(keyword)

    for employee in employees:

        employee_table.insert(
            "",
            "end",
            values=(
                employee["employee_id"],
                employee["name"],
                employee["department"],
                employee["salary"],
                employee["status"]
            )
        )


def update_employee():

    selected = employee_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an employee from the table."
        )

        return

    employee = employee_table.item(selected[0])

    employee_id = employee["values"][0]

    name = name_entry.get().strip()
    department = department_combobox.get()
    salary = salary_entry.get().strip()
    status = status_combobox.get()

    if not name or not department or not salary:

        messagebox.showwarning(
            "Missing Information",
            "Please fill in all employee fields."
        )

        return

    updated_data = {
        "name": name,
        "department": department,
        "salary": salary,
        "status": status
    }

    update_employee_database(
        employee_id,
        updated_data
    )

    load_employees()

    clear_fields()

    messagebox.showinfo(
        "Success",
        f"Employee {employee_id} updated successfully."
    )


def delete_employee():

    selected = employee_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an employee from the table."
        )

        return

    employee = employee_table.item(selected[0])

    employee_id = employee["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete {employee_id}?"
    )

    if not confirm:
        return

    delete_employee_database(employee_id)

    load_employees()

    clear_fields()

    messagebox.showinfo(
        "Success",
        f"Employee {employee_id} deleted successfully."
    )


def clear_fields():

    name_entry.delete(0, tk.END)

    if department_combobox["values"]:
        department_combobox.current(0)

    salary_entry.delete(0, tk.END)

    status_combobox.current(0)

    username_entry.delete(0, tk.END)

    password_entry.delete(0, tk.END)


def load_employees():

    # Remove existing rows
    employee_table.delete(
        *employee_table.get_children()
    )

    # Get employees from MongoDB
    employees = get_all_employees()

    # Display employees
    for employee in employees:

        employee_table.insert(
            "",
            "end",
            values=(
                employee["employee_id"],
                employee["name"],
                employee["department"],
                employee["salary"],
                employee["status"]
            )
        )


def load_departments():

    departments = get_all_departments()

    department_names = []

    for department in departments:

        department_names.append(
            department["name"]
        )

    department_combobox["values"] = department_names

    if department_names:
        department_combobox.current(0)


def logout():

    root.destroy()

    import login



# MAIN WINDOW


root = tk.Tk()

root.title("Employee Management System")
root.state("zoomed")
root.resizable(False, False)
root.configure(bg=COLOR_BG)

configure_ttk_style()

# TITLE

title_label = tk.Label(
    root,
    text="EMPLOYEE MANAGEMENT SYSTEM",
    font=FONT_TITLE,
    bg=COLOR_BG,
    fg=COLOR_TEXT
)
title_label.pack(pady=10)

# MAIN FRAME


main_frame = tk.Frame(root, bg=COLOR_BG)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# FORM FRAME

form_frame = styled_labelframe(main_frame, text="Employee Info", padx=10, pady=10)
form_frame.pack(side="left", fill="y")


# Full Name
tk.Label(form_frame, text="Full Name", bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=2, column=0, sticky="w")
name_entry = styled_entry(form_frame, width=30)
name_entry.grid(row=3,column=0,pady=5)

# Department
tk.Label(form_frame, text="Department", bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=4, column=0, sticky="w")
department_combobox = ttk.Combobox(form_frame,width=27,state="readonly")
department_combobox.grid(row=5,column=0,pady=5)

# Salary
tk.Label(form_frame, text="Salary", bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=6, column=0, sticky="w")

salary_entry = styled_entry(form_frame, width=30)
salary_entry.grid(row=7, column=0, pady=5)

# Status
tk.Label(form_frame, text="Status", bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=8, column=0, sticky="w")
status_combobox = ttk.Combobox(form_frame,values=["Active", "On Leave", "Resigned"],width=27)

status_combobox.grid(row=9, column=0, pady=5)
status_combobox.current(0)

# Username

tk.Label(form_frame, text="Username", bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=10, column=0, sticky="w")
username_entry = styled_entry(form_frame, width=30)
username_entry.grid(row=11,column=0,pady=5)
# Temporary Password

tk.Label(form_frame, text="Temporary Password", bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=12, column=0, sticky="w")

password_entry = styled_entry(form_frame, width=30, show="*")

password_entry.grid(row=13,column=0,pady=5)

# Buttons
add_button = styled_button(form_frame, text="Add Employee", command=add_employee, bg=COLOR_PRIMARY, active_bg=COLOR_PRIMARY_DARK)
add_button.grid(row=14, column=0, pady=10)

update_button = styled_button(form_frame, text="Update Employee", command=update_employee, bg=COLOR_SUCCESS, active_bg=COLOR_SUCCESS_DARK)
update_button.grid(row=15, column=0, pady=5)

delete_button = styled_button(form_frame, text="Delete Employee", command=delete_employee, bg=COLOR_DANGER, active_bg=COLOR_DANGER_DARK)
delete_button.grid(row=16, column=0, pady=5)

logout_button = styled_button(form_frame, text="Logout", command=logout, bg=COLOR_DANGER, active_bg=COLOR_DANGER_DARK)
logout_button.grid(row=17,column=0,pady=15)

#SEARCH FRAME

search_frame = tk.Frame(main_frame, bg=COLOR_BG)

search_frame.pack(
    fill="x",
    pady=10
)

tk.Label(
    search_frame,
    text="Search Employee:",
    bg=COLOR_BG,
    fg=COLOR_TEXT
).pack(
    side="left",
    padx=5
)

search_entry = styled_entry(
    search_frame,
    width=30
)

search_entry.pack(
    side="left",
    padx=5
)

search_button = styled_button(
    search_frame,
    text="Search",
    command=search_employee,
    bg=COLOR_PRIMARY,
    active_bg=COLOR_PRIMARY_DARK,
    width=12
)

search_button.pack(
    side="left",
    padx=5
)
#RESET BUTTON FOR THE SEARCH BAR
reset_button = styled_button(
    search_frame,
    text="Show All",
    command=load_employees,
    bg=COLOR_NEUTRAL,
    active_bg=COLOR_NEUTRAL_DARK,
    width=12
)

reset_button.config(fg=COLOR_TEXT, activeforeground=COLOR_TEXT)

reset_button.pack(
    side="left",
    padx=5
)

# TABLE FRAME


table_frame = styled_labelframe(
    main_frame,
    text="Employee Records",
    padx=10,
    pady=10
)

table_frame.pack(
    side="right",
    fill="both",
    expand=True
)

# Table Columns
columns = (
    "ID",
    "Name",
    "Department",
    "Salary",
    "Status"
)

employee_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)
employee_table.bind(
    "<<TreeviewSelect>>",
    select_employee
)

for col in columns:
    employee_table.heading(col, text=col)
    employee_table.column(col, width=140)

# Scrollbar
scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=employee_table.yview
)

employee_table.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(side="right", fill="y")
employee_table.pack(fill="both", expand=True)

# Load departments from MongoDB
load_departments()

# Load employees from MongoDB
load_employees()

# RUN APPLICATION

if __name__ == "__main__":
    root.mainloop()