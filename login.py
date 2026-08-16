import tkinter as tk
from tkinter import messagebox

from database import login_user

# -----------------------------------------------------------------
# STYLE CONSTANTS (same palette as the other StaffSync screens)
# -----------------------------------------------------------------

COLOR_BG = "#F1F5F9"          # page background
COLOR_CARD = "#FFFFFF"        # card / panel background
COLOR_BORDER = "#CBD5E1"      # card border
COLOR_TEXT = "#0F172A"        # main text
COLOR_MUTED = "#64748B"       # secondary text

COLOR_PRIMARY = "#2563EB"
COLOR_PRIMARY_DARK = "#1E40AF"

# Font unchanged from the original file
FONT_TITLE = ("Arial", 22, "bold")


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


def styled_button(parent, text, command, bg=COLOR_PRIMARY, active_bg=COLOR_PRIMARY_DARK, width=20):

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


def open_dashboard(user):

    role = user["role"]

    root.destroy()

    if role == "admin":

        import admin_dashboard

    elif role == "employee":

        import employee_dashboard

        employee_dashboard.start_dashboard(
            user["employee_id"],
            user["username"]
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
root.configure(bg=COLOR_BG)


# TITLE

tk.Label(
    root,
    text="STAFFSYNC",
    font=FONT_TITLE,
    bg=COLOR_BG,
    fg=COLOR_TEXT
).pack(pady=20)

# USERNAME

tk.Label(root, text="Username", bg=COLOR_BG, fg=COLOR_TEXT).pack()
username_entry = styled_entry(root, width=30)
username_entry.pack(pady=5)

# PASSWORD

tk.Label(root, text="Password", bg=COLOR_BG, fg=COLOR_TEXT).pack()
password_entry = styled_entry(root, width=30, show="*")
password_entry.pack(pady=5)

# LOGIN BUTTON

styled_button(root, text="Login", command=login, width=20).pack(pady=20)

# RUN APPLICATION

if __name__ == "__main__":
    root.mainloop()