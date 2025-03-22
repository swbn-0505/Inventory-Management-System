import tkinter as tk
from tkinter import messagebox
import sqlite3
from manage_users import manage_users
from administrator import manage_inventory
from salesman import open_salesman_window, open_billing_window , report_inventory_issue , report_exception_issue
from inventory_manager import check_inventory_status , view_sales_reports , generate_reports , generate_sales_report
from sales_manager import get_bills_today , open_sales_trend_window , generate_sales_trends , view_exception_reports

# Function to create the dashboard
def open_dashboard(username, role):
    dashboard = tk.Tk()
    dashboard.title(f"{role} Dashboard - Inventory Management System")
    dashboard.geometry("600x500")

    tk.Label(dashboard, text=f"Welcome, {username}!", font=("Arial", 14)).pack(pady=10)
    tk.Label(dashboard, text=f"Role: {role}", font=("Arial", 12)).pack(pady=5)

    if role == "Admin":
        tk.Button(dashboard, text="Manage Users", font=("Arial", 12), command=manage_users).pack(pady=5)
        tk.Button(dashboard, text="Manage Inventory", font=("Arial", 12), command=manage_inventory).pack(pady=5)
    elif role == "Salesman":
        tk.Button(dashboard, text="Search Inventory", font=("Arial", 12), command=open_salesman_window).pack(pady=5)
        tk.Button(dashboard, text="Generate Bill", font=("Arial", 12), command=open_billing_window).pack(pady=5)
        tk.Button(dashboard, text="Report Inventory Issue", font=("Arial", 12), command=report_inventory_issue).pack(pady=5)
        tk.Button(dashboard, text="Report Exception Issue", font=("Arial", 12), command=report_exception_issue).pack(pady=5)

    elif role == "Inventory Manager":
        tk.Button(dashboard, text="Check Inventory Status", font=("Arial", 12), command=check_inventory_status).pack(pady=5)
        tk.Button(dashboard, text="View Sales Reports", font=("Arial", 12), command=view_sales_reports).pack(pady=5)
        tk.Button(dashboard, text="Generate Inventory Reports", font=("Arial", 12), command=generate_reports).pack(pady=5)
        tk.Button(dashboard, text="Generate Sales Report", font=("Arial", 12), command= generate_sales_report).pack(pady=5)

    elif role == "Sales Manager":
        tk.Button(dashboard, text="Check Bills Generated", font=("Arial", 12), command=get_bills_today).pack(pady=5)
        tk.Button(dashboard, text="Sales Trend", font=("Arial", 12), command=open_sales_trend_window).pack(pady=5)
        tk.Button(dashboard, text="Overall Sales Trend", font=("Arial", 12), command=generate_sales_trends).pack(pady=5)
        tk.Button(dashboard, text="Check exception reports", font=("Arial", 12), command=view_exception_reports).pack(pady=5)

    tk.Button(dashboard, text="Logout", font=("Arial", 12), command=dashboard.destroy).pack(pady=20)

    dashboard.mainloop()

