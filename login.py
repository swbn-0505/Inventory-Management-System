import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from dashboard import open_dashboard  # Importing the dashboard function

# Function to verify login
def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Login Successful", f"Welcome, {username} ({result[0]})")
        root.destroy()  # Close login window
        open_dashboard(username, result[0])  # Open dashboard based on role
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# Toggle Password Visibility
def toggle_password():
    if entry_password.cget("show") == "*":
        entry_password.config(show="")
        show_password_btn.config(text="👁 Hide")
    else:
        entry_password.config(show="*")
        show_password_btn.config(text="👁 Show")

# Create login window
root = tk.Tk()
root.title("Login - Inventory Management System")
root.geometry("500x400")  # Increased window size
root.resizable(False, False)
root.configure(bg="#1E1E1E")  # Dark professional background

# Frame for UI elements
frame = tk.Frame(root, bg="#2C2F33", padx=25, pady=25, relief="solid", bd=1)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title Label
tk.Label(frame, text="LOGIN", font=("Arial", 18, "bold"), bg="#2C2F33", fg="#00BFFF").pack(pady=(0, 15))

# Username Label & Entry
tk.Label(frame, text="Username:", font=("Arial", 12), bg="#2C2F33", fg="white").pack(anchor="w")
entry_username = ttk.Entry(frame, font=("Arial", 12), width=30)
entry_username.pack(pady=5)

# Password Label & Entry with toggle button
tk.Label(frame, text="Password:", font=("Arial", 12), bg="#2C2F33", fg="white").pack(anchor="w")
pass_frame = tk.Frame(frame, bg="#2C2F33")
entry_password = ttk.Entry(pass_frame, font=("Arial", 12), width=24, show="*")
entry_password.pack(side="left", padx=(0, 5))
show_password_btn = ttk.Button(pass_frame, text="👁 Show", width=7, command=toggle_password)
show_password_btn.pack(side="left")
pass_frame.pack(pady=5)

# Login Button
ttk.Button(frame, text="Login", command=login, style="Login.TButton").pack(pady=15)

# Style Configuration
style = ttk.Style()
style.configure("Login.TButton", font=("Arial", 13, "bold"), background="#00BFFF", foreground="black", padding=8)

root.mainloop()

