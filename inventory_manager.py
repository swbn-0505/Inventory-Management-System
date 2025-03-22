import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# Function to check inventory status
def check_inventory_status():
    status_window = tk.Toplevel()
    status_window.title("Inventory Status")
    status_window.geometry("1000x400")

    tk.Label(status_window, text="Current Inventory Status", font=("Arial", 14)).pack(pady=10)

    # Create Treeview (table-like structure)
    columns = ("ID", "Item Name", "Category", "Price", "Quantity")
    inventory_tree = ttk.Treeview(status_window, columns=columns, show="headings")
    inventory_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Define column headings
    for col in columns:
        inventory_tree.heading(col, text=col)
        inventory_tree.column(col, anchor="center")

    # Fetch inventory data from database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()

    # Insert data into treeview
    for item in items:
        inventory_tree.insert("", "end", values=item)

    status_window.mainloop()

def view_sales_reports():
    report_window = tk.Toplevel()
    report_window.title("Sales Reports")
    report_window.geometry("600x400")

    tk.Label(report_window, text="Reported Inventory Issues", font=("Arial", 14)).pack(pady=10)

    report_list = tk.Listbox(report_window, font=("Arial", 12), width=80, height=15)
    report_list.pack(pady=10)

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_name, issue FROM sales_reports WHERE resolved = 0")
    reports = cursor.fetchall()
    conn.close()

    for report in reports:
        report_list.insert(tk.END, f"{report[0]}. {report[1]} - Issue: {report[2]}")

    def mark_resolved():
        selected = report_list.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a report to mark as resolved!")
            return

        report_id = report_list.get(selected[0]).split(".")[0]  # Extract ID
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE sales_reports SET resolved = 1 WHERE id=?", (report_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Report marked as resolved!")
        report_list.delete(selected[0])  # Remove from listbox

    tk.Button(report_window, text="Mark as Resolved", font=("Arial", 12), command=mark_resolved).pack(pady=10)

## Generate reports

def generate_reports():
    report_window = tk.Toplevel()
    report_window.title("Inventory Reports")
    report_window.geometry("600x400")

    tk.Label(report_window, text="Generate Inventory Reports", font=("Arial", 14)).pack(pady=10)

    # Report Type Selection
    tk.Label(report_window, text="Select Report Type:", font=("Arial", 12)).pack(pady=5)
    report_type = ttk.Combobox(report_window, values=["Category-wise", "Price-wise"], state="readonly", font=("Arial", 12))
    report_type.pack(pady=5)
    report_type.set("Category-wise")

    # Treeview to display report
    report_tree = ttk.Treeview(report_window, columns=("ID", "Name", "Category", "Price", "Quantity"), show="headings")
    report_tree.heading("ID", text="ID")
    report_tree.heading("Name", text="Name")
    report_tree.heading("Category", text="Category")
    report_tree.heading("Price", text="Price")
    report_tree.heading("Quantity", text="Quantity")
    report_tree.column("ID", width=40)
    report_tree.column("Name", width=120)
    report_tree.column("Category", width=100)
    report_tree.column("Price", width=80)
    report_tree.column("Quantity", width=80)
    report_tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def load_report():
        report_tree.delete(*report_tree.get_children())  # Clear previous data
        report_option = report_type.get()

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        if report_option == "Category-wise":
            cursor.execute("SELECT * FROM inventory ORDER BY category")
        elif report_option == "Price-wise":
            cursor.execute("SELECT * FROM inventory ORDER BY price")

        records = cursor.fetchall()
        conn.close()

        for record in records:
            report_tree.insert("", tk.END, values=record)

    tk.Button(report_window, text="Generate Report", font=("Arial", 12), command=load_report).pack(pady=10)

    report_window.mainloop()

def generate_sales_report():
    report_window = tk.Toplevel()
    report_window.title("Sales Report")
    report_window.geometry("600x500")

    tree = ttk.Treeview(report_window, columns=("Item Name", "Total Price","Quantity Sold", "Sale Date"), show="headings")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Total Price", text="Total Price (₹)")
    tree.heading("Quantity Sold", text="Quantity Sold")
    # tree.heading("Price per Unit", text="Price per Unit (₹)")
    tree.heading("Sale Date", text="Sale Date")

    tree.column("Item Name", width=150)
    tree.column("Total Price", width=100)
    tree.column("Quantity Sold", width=100)
    # tree.column("Price per Unit", width=120)
    tree.column("Sale Date", width=100)

    tree.pack(expand=True, fill="both")

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    query = "SELECT * FROM sales ORDER BY price DESC"

    cursor.execute(query)
    sales_data = cursor.fetchall()
    conn.close()

    for sale in sales_data:
        tree.insert("", tk.END, values=(sale[1], sale[2], sale[3], sale[4]))

    messagebox.showinfo("Success", f"Sales Report Generated Successfully!")