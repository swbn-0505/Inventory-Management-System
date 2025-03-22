import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to open search inventory window
def open_salesman_window():
    search_window = tk.Toplevel()
    search_window.title("Search Inventory")
    search_window.geometry("600x400")

    tk.Label(search_window, text="Search by Name or Category:", font=("Arial", 12)).pack(pady=5)
    search_entry = tk.Entry(search_window, font=("Arial", 12))
    search_entry.pack(pady=5)

    result_list = tk.Listbox(search_window, font=("Arial", 12), width=60, height=10)
    result_list.pack(pady=10)

    def search_inventory():
        query = search_entry.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a search term!")
            return
        
        result_list.delete(0, tk.END)
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE name LIKE ? OR category LIKE ?", ('%' + query + '%', '%' + query + '%'))
        items = cursor.fetchall()
        conn.close()
        
        if items:
            for item in items:
                result_list.insert(tk.END, f"{item[0]}. {item[1]} - {item[2]} - ₹{item[3]} - Qty: {item[4]}")
        else:
            messagebox.showinfo("No Results", "No items found matching the search term.")

    tk.Button(search_window, text="Search", font=("Arial", 12), command=search_inventory).pack(pady=5)

# Function to open billing window
def open_billing_window():
    bill_window = tk.Toplevel()
    bill_window.title("Generate Bill")
    bill_window.geometry("700x700")

    tk.Label(bill_window, text="Select Items for Billing:", font=("Arial", 12)).pack(pady=5)
    item_list = tk.Listbox(bill_window, font=("Arial", 12), width=60, height=10)
    item_list.pack(pady=10)

    cart = []
    inventory_items = {}

    # Load inventory items
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()
    
    for item in items:
        item_id = str(item[0])
        item_list.insert(tk.END, f"{item_id}. {item[1]} - ₹{item[3]} - Qty: {item[4]}")
        inventory_items[item_id] = {"name": item[1], "price": item[3], "quantity": item[4]}

    quantity_entry = tk.Entry(bill_window, font=("Arial", 12), width=5)
    quantity_entry.pack(pady=5)
    quantity_entry.insert(0, "1")

    def add_to_cart():
        selected_item = item_list.get(tk.ACTIVE)
        if not selected_item:
            messagebox.showerror("Error", "Select an item to add to the bill!")
            return
        
        item_id = selected_item.split(".")[0]
        if item_id not in inventory_items:
            messagebox.showerror("Error", "Invalid item selection!")
            return

        item_data = inventory_items[item_id]
        item_name, item_price, available_quantity = item_data["name"], item_data["price"], item_data["quantity"]
        
        try:
            qty = int(quantity_entry.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid quantity!")
            return
        
        if qty > available_quantity:
            messagebox.showerror("Error", f"Only {available_quantity} items available in stock!")
            return

        cart.append({"id": item_id, "name": item_name, "price": item_price, "quantity": qty})
        cart_list.insert(tk.END, f"{item_name} x{qty} - ₹{item_price * qty}")

    # Remove item from cart
    def remove_from_cart():
        selected_cart_item = cart_list.get(tk.ACTIVE)
        if not selected_cart_item:
            messagebox.showerror("Error", "Select an item to remove from the cart!")
            return
        
        item_name = selected_cart_item.split(" x")[0]
        for item in cart:
            if item["name"] == item_name:
                item_id, qty = item["id"], item["quantity"]
                cart.remove(item)
                cart_list.delete(tk.ACTIVE)

                # Restore stock quantity in inventory
                inventory_items[item_id]["quantity"] += qty
                reload_inventory()
                return


    def generate_bill():
        if not cart:
            messagebox.showerror("Error", "No items in the cart!")
            return
        
        total_amount = sum(item["price"] * item["quantity"] for item in cart)
        bill_text = "\n".join([f"{item['name']} x{item['quantity']} - ₹{item['price'] * item['quantity']}" for item in cart])

        # Deduct items from inventory
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        for item in cart:
            item_name = item["name"]
            #category = item["category"]
            price = item["price"]*item["quantity"]
            quantity_sold = item["quantity"]

        # Insert the sold item into the sales table
            cursor.execute(
            "INSERT INTO sales (item_name, price, quantity_sold, date_sold) VALUES (?, ?, ?, DATE('now'))",
            (item_name, price, quantity_sold)
        )
            cursor.execute("UPDATE inventory SET quantity = quantity - ? WHERE id = ?", (item["quantity"], item["id"]))
        conn.commit()
        conn.close()

        messagebox.showinfo("Bill", f"Items Purchased:\n{bill_text}\n\nTotal Amount: ₹{total_amount}")
        cart.clear()
        cart_list.delete(0, tk.END)
        item_list.delete(0, tk.END)
        reload_inventory()
    
    def reload_inventory():
        """Reloads inventory items after sales to show updated stock"""
        item_list.delete(0, tk.END)
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        items = cursor.fetchall()
        conn.close()
        for item in items:
            item_id = str(item[0])
            item_list.insert(tk.END, f"{item_id}. {item[1]} - ₹{item[3]} - Qty: {item[4]}")
            inventory_items[item_id]["quantity"] = item[4]

    cart_list = tk.Listbox(bill_window, font=("Arial", 12), width=50, height=5)
    cart_list.pack(pady=10)

    tk.Button(bill_window, text="Add to Bill", font=("Arial", 12), command=add_to_cart).pack(pady=5)
    tk.Button(bill_window, text="Remove from Cart", font=("Arial", 12), command=remove_from_cart).pack(pady=5)
    tk.Button(bill_window, text="Generate Bill", font=("Arial", 12), command=generate_bill).pack(pady=5)

def report_inventory_issue():
    """Opens a window for salespeople to report inventory issues."""

    issue_window = tk.Toplevel()
    issue_window.title("Report Inventory Issue")
    issue_window.geometry("400x300")

    tk.Label(issue_window, text="Item Name:", font=("Arial", 12)).pack(pady=5)
    entry_item = tk.Entry(issue_window, font=("Arial", 12))
    entry_item.pack(pady=5)

    tk.Label(issue_window, text="Issue Description:", font=("Arial", 12)).pack(pady=5)
    entry_issue = tk.Entry(issue_window, font=("Arial", 12))
    entry_issue.pack(pady=5)

    def submit_issue():
        item_name = entry_item.get().strip()
        issue_text = entry_issue.get().strip()

        if not item_name or not issue_text:
            messagebox.showerror("Error", "Both fields are required!")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sales_reports (item_name, issue , resolved) VALUES (?, ? , 0)", (item_name, issue_text))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Issue reported successfully!")
        issue_window.destroy()

    tk.Button(issue_window, text="Submit Report", font=("Arial", 12), command=submit_issue).pack(pady=10)

#Report exception issue
def report_exception_issue():
    """Opens a window for salespeople to report exception issues."""

    issue_window = tk.Toplevel()
    issue_window.title("Report Exception Issue")
    issue_window.geometry("400x300")

    tk.Label(issue_window, text="Item Name:", font=("Arial", 12)).pack(pady=5)
    entry_item = tk.Entry(issue_window, font=("Arial", 12))
    entry_item.pack(pady=5)

    tk.Label(issue_window, text="Issue Description:", font=("Arial", 12)).pack(pady=5)
    entry_issue = tk.Entry(issue_window, font=("Arial", 12))
    entry_issue.pack(pady=5)

    def submit_issue():
        item_name = entry_item.get().strip()
        issue_text = entry_issue.get().strip()

        if not item_name or not issue_text:
            messagebox.showerror("Error", "Both fields are required!")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO exception_reports (item_name, issue , resolved) VALUES (?, ? , 0)", (item_name, issue_text))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Issue reported successfully!")
        issue_window.destroy()

    tk.Button(issue_window, text="Submit Report", font=("Arial", 12), command=submit_issue).pack(pady=10)
