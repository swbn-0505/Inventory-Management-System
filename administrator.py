import tkinter as tk
from tkinter import messagebox
import sqlite3

def manage_inventory():
    inventory_window = tk.Toplevel()
    inventory_window.title("Manage Inventory")
    inventory_window.geometry("600x400")

    tk.Label(inventory_window, text="Item Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(inventory_window, font=("Arial", 12))
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(inventory_window, text="Category:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    entry_category = tk.Entry(inventory_window, font=("Arial", 12))
    entry_category.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(inventory_window, text="Price:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    entry_price = tk.Entry(inventory_window, font=("Arial", 12))
    entry_price.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(inventory_window, text="Quantity:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    entry_quantity = tk.Entry(inventory_window, font=("Arial", 12))
    entry_quantity.grid(row=3, column=1, padx=10, pady=5)

    # Function to add item
    def add_item():
        name = entry_name.get()
        category = entry_category.get()
        price = entry_price.get()
        quantity = entry_quantity.get()

        if not name or not category or not price or not quantity:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and quantity must be an integer!")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (name, category, price, quantity) VALUES (?, ?, ?, ?)", (name, category, price, quantity))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Item added successfully!")
        entry_name.delete(0, tk.END)
        entry_category.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        load_inventory()  # Refresh inventory list
    # Function to load selected item into entry fields
    def select_item(event):
        selected_item = inventory_list.get(tk.ACTIVE)
        if not selected_item:
            return
        
        item_id = selected_item.split(".")[0]  # Extract ID
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE id=?", (item_id,))
        item = cursor.fetchone()
        conn.close()

        if item:
            entry_name.delete(0, tk.END)
            entry_category.delete(0, tk.END)
            entry_price.delete(0, tk.END)
            entry_quantity.delete(0, tk.END)

            entry_name.insert(0, item[1])
            entry_category.insert(0, item[2])
            entry_price.insert(0, item[3])
            entry_quantity.insert(0, item[4])

    # Function to update item
    def update_item():
        selected_item = inventory_list.get(tk.ACTIVE)
        if not selected_item:
            messagebox.showerror("Error", "Select an item to update!")
            return

        item_id = selected_item.split(".")[0]  # Extract ID
        name = entry_name.get()
        category = entry_category.get()
        price = entry_price.get()
        quantity = entry_quantity.get()

        if not name or not category or not price or not quantity:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and quantity must be an integer!")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET name=?, category=?, price=?, quantity=? WHERE id=?", 
                       (name, category, price, quantity, item_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Item updated successfully!")
        load_inventory()  # Refresh inventory list

    # Function to load inventory
    def load_inventory():
        inventory_list.delete(0, tk.END)
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        items = cursor.fetchall()
        conn.close()
        for item in items:
            inventory_list.insert(tk.END, f"{item[0]}. {item[1]} - {item[2]} - ₹{item[3]} - Qty: {item[4]}")

    # Function to delete item
    def delete_item():
        selected_item = inventory_list.get(tk.ACTIVE)
        if not selected_item:
            messagebox.showerror("Error", "Select an item to delete!")
            return

        item_id = selected_item.split(".")[0]

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Item deleted successfully!")
        load_inventory()  # Refresh inventory list

    # Buttons
    tk.Button(inventory_window, text="Add Item", font=("Arial", 12), command=add_item).grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(inventory_window, text="Update Item", font=("Arial", 12), command=update_item).grid(row=5, column=0, columnspan=2, pady=5)
    tk.Button(inventory_window, text="Delete Item", font=("Arial", 12), command=delete_item).grid(row=5, column=1, columnspan=2, pady=5)

    # Inventory List
    inventory_list = tk.Listbox(inventory_window, font=("Arial", 12), width=60, height=10)
    inventory_list.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    inventory_list.bind("<<ListboxSelect>>", select_item)  # Bind selection event

    load_inventory()  # Load inventory when opening
