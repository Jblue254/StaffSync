import tkinter as tk
from tkinter import ttk

root = tk.Tk()

root.title("Employee Management System")

root.geometry("1200x700")

root.resizable(False, False)

title_label = tk.Label(
    root,
    text="EMPLOYEE MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold")   
)
title_label.pack(pady=10)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

form_frame = tk.LabelFrame(main_frame)
table_frame = tk.LabelFrame(main_frame)

form_frame = tk.LabelFrame(
    main_frame,
    text="Employee Information",
    padx=10,
    pady=10
)

form_frame.pack(
    side="left",
    fill="y"
)

table_frame = tk.LabelFrame(
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

tk.Label(
    form_frame,
    text="Employee ID"
).grid(
    row=0,
    column=0,
    sticky="w"
)

employee_id_entry = tk.Entry(
    form_frame,
    width=30
)

employee_id_entry.grid(
    row=1,
    column=0,
    pady=5
)

tk.Label(
    form_frame,
    text="Full Name"
).grid(
    row=2,
    column=0,
    sticky="w"
)

name_entry = tk.Entry(
    form_frame,
    width=30
)

name_entry.grid(
    row=3,
    column=0,
    pady=5
)

tk.Label(
    form_frame,
    text="Department"
).grid(
    row=4,
    column=0,
    sticky="w"
)

department_entry = tk.Entry(
    form_frame,
    width=30
)

department_entry.grid(
    row=5,
    column=0,
    pady=5
)

tk.Label(
    form_frame,
    text="Salary"
).grid(
    row=6,
    column=0,
    sticky="w"
)

salary_entry = tk.Entry(
    form_frame,
    width=30
)

salary_entry.grid(
    row=7,
    column=0,
    pady=5
)

tk.Label(
    form_frame,
    text="Status"
).grid(
    row=8,
    column=0,
    sticky="w"
)

status_combobox = ttk.Combobox(
    form_frame,
    values=[
        "Active",
        "On Leave",
        "Resigned"
    ],
    width=27
)

status_combobox.grid(
    row=9,
    column=0,
    pady=5
)