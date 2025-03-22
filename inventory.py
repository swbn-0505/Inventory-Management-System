import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create database & table (Runs only once)
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    )
""")
conn.commit()
conn.close()

# Function to add a new item
def add_item():
    item_name = item_name_entry.get()
    category = category_entry.get()
    price = price_entry.get()

    if not item_name or not category or not price:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (item_name, category, price) VALUES (?, ?, ?)", (item_name, category, float(price)))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Item added successfully!")
        item_name_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        view_items()  # Refresh inventory list

    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Function to delete an item
def delete_item():
    selected_item = item_listbox.curselection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to delete!")
        return

    item_id = item_listbox.get(selected_item).split(" - ")[0]  # Extract item ID

    try:
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Item deleted successfully!")
        view_items()  # Refresh inventory list

    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")

# Function to view inventory items
def view_items():
    item_listbox.delete(0, tk.END)  # Clear the listbox

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()

    for item in items:
        item_listbox.insert(tk.END, f"{item[0]} - {item[1]} ({item[2]}) - ${item[3]}")

# Function to open inventory management window
def open_inventory():
    global item_name_entry, category_entry, price_entry, item_listbox

    inventory_window = tk.Toplevel()
    inventory_window.title("Inventory Management")
    inventory_window.geometry("500x500")

    tk.Label(inventory_window, text="Item Name:").pack()
    item_name_entry = tk.Entry(inventory_window)
    item_name_entry.pack()

    tk.Label(inventory_window, text="Category:").pack()
    category_entry = tk.Entry(inventory_window)
    category_entry.pack()

    tk.Label(inventory_window, text="Price:").pack()
    price_entry = tk.Entry(inventory_window)
    price_entry.pack()

    tk.Button(inventory_window, text="Add Item", command=add_item).pack(pady=5)
    tk.Button(inventory_window, text="Delete Selected Item", command=delete_item).pack(pady=5)

    tk.Label(inventory_window, text="Inventory List:").pack()
    item_listbox = tk.Listbox(inventory_window, width=50)
    item_listbox.pack()

    view_items()  # Load existing items into the list

# Testing: Uncomment the below line to test this module separately
# open_inventory()

