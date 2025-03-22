import tkinter as tk
from tkinter import messagebox
import sqlite3

def manage_users():
    user_window = tk.Toplevel()
    user_window.title("Manage Users")
    user_window.geometry("600x400")

    tk.Label(user_window, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    entry_username = tk.Entry(user_window, font=("Arial", 12))
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(user_window, text="Role:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    entry_role = tk.Entry(user_window, font=("Arial", 12))
    entry_role.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(user_window, text="Password:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    entry_password = tk.Entry(user_window, font=("Arial", 12), show="*")
    entry_password.grid(row=2, column=1, padx=10, pady=5)

    # Function to add user
    def add_user():
        username = entry_username.get()
        role = entry_role.get()
        password = entry_password.get()

        if not username or not role or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, role, password) VALUES (?, ?, ?)", (username, role, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "User added successfully!")
        entry_username.delete(0, tk.END)
        entry_role.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        load_users()

    # Function to load users
    def load_users():
        user_list.delete(0, tk.END)
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        for user in users:
            user_list.insert(tk.END, f"{user[0]}. {user[1]} - {user[2]}")

    # Function to delete user
    def delete_user():
        selected_user = user_list.get(tk.ACTIVE)
        if not selected_user:
            messagebox.showerror("Error", "Select a user to delete!")
            return

        user_id = selected_user.split(".")[0]

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "User deleted successfully!")
        load_users()

    # Function to update user
    def update_user():
        selected_user = user_list.get(tk.ACTIVE)
        if not selected_user:
            messagebox.showerror("Error", "Select a user to update!")
            return

        user_id = selected_user.split(".")[0]
        username = entry_username.get()
        role = entry_role.get()
        password = entry_password.get()

        if not username or not role or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username=?, role=?, password=? WHERE id=?", (username, role, password, user_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "User updated successfully!")
        entry_username.delete(0, tk.END)
        entry_role.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        load_users()

    # Buttons
    tk.Button(user_window, text="Add User", font=("Arial", 12), command=add_user).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(user_window, text="Delete User", font=("Arial", 12), command=delete_user).grid(row=4, column=0, columnspan=2, pady=5)
    tk.Button(user_window, text="Update User", font=("Arial", 12), command=update_user).grid(row=5, column=0, columnspan=2, pady=5)

    # User List
    user_list = tk.Listbox(user_window, font=("Arial", 12), width=60, height=10)
    user_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    load_users()  # Load users when opening
