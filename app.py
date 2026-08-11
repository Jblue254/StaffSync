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





