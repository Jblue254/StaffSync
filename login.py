import tkinter as tk
from tkinter import messagebox

from database import login_user


def login():

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Missing Information", "Please enter username and password.")
        return

    user = login_user(username, password)

    if user is None:

        messagebox.showerror("Login Failed","Invalid username or password.")

        return

    role = user["role"]

    messagebox.showinfo("Login Successful",f"Welcome {username}!\nRole: {role}")

    root.destroy()

# LOGIN WINDOW

root = tk.Tk()

root.title("StaffSync Login")
root.geometry("400x300")
root.resizable(False, False)


# Title

tk.Label(root,text="STAFFSYNC",font=("Arial", 22, "bold")).pack(pady=20)


# Username

tk.Label(root,text="Username").pack()

username_entry = tk.Entry(root,width=30)

username_entry.pack(pady=5)


# Password

tk.Label(root,text="Password").pack()

password_entry = tk.Entry(root,width=30,show="*")

password_entry.pack(pady=5)

# Login button

login_button = tk.Button(root,text="Login",width=20,command=login)

login_button.pack(pady=20)


root.mainloop()