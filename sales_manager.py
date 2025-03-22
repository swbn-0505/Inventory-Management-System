import sqlite3
from datetime import datetime
from tkinter import Tk, Label, Toplevel, ttk, messagebox
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import pandas as pd

# Generate Bills
def get_bills_today():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    today_date = datetime.now().strftime("%Y-%m-%d")

    # Get total count of bills and total amount of sales today
    cursor.execute("SELECT COUNT(DISTINCT id), SUM(price) FROM sales WHERE date_sold = ?", (today_date,))
    result = cursor.fetchone()
    bill_count = result[0] if result[0] else 0
    total_sales  = result[1] if result[1] else 0.0

    # Get all bills generated today
    cursor.execute("SELECT DISTINCT id, item_name , price, date_sold FROM sales WHERE date_sold = ?", (today_date,))
    bills = cursor.fetchall()

    conn.close()

    # Show result in a new window
    show_bills_window(bill_count,total_sales,bills)

def show_bills_window(bill_count,total_sales, bills):
    bill_window = Toplevel()
    bill_window.title("Today's Bills")

    # Show total bills count
    Label(bill_window, text=f"Total Bills Generated Today: {bill_count}", font=("Arial", 12, "bold")).pack(pady=5)
    Label(bill_window, text=f"Total Sales Amount Today: ₹{total_sales :.2f}", font=("Arial", 12, "bold")).pack(pady=5)


    # Create Table to display bills
    columns = ("Bill ID", "Item Name" , "Total Amount", "Date Sold")
    tree = ttk.Treeview(bill_window, columns=columns, show="headings")
    tree.heading("Bill ID", text="Bill ID")
    tree.heading("Item Name" , text = "Item Name")
    tree.heading("Total Amount", text="Total Amount")
    tree.heading("Date Sold", text="Date Sold")

    # Insert data into table
    for bill in bills:
        tree.insert("", "end", values=bill)

    tree.pack(pady=10)


# Function to fetch unique items from sales data
def get_items():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT item_name FROM sales")  
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return items

# Function to fetch sales data based on item and timeframe
def fetch_sales_data(item, timeframe):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Determine the date range
    today = datetime.now().date()
    if timeframe == "Daily":
        start_date = today
    elif timeframe == "Weekly":
        start_date = today - timedelta(days=7)
    else:  # Monthly
        start_date = today - timedelta(days=30)

    query = """
        SELECT date_sold, SUM(quantity_sold) FROM sales
        WHERE item_name = ? AND date_sold >= ?
        GROUP BY date_sold
        ORDER BY date_sold
    """
    cursor.execute(query, (item, start_date))
    data = cursor.fetchall()
    conn.close()

    return data

# Function to plot sales trend
def plot_sales_trend(item, timeframe):
    data = fetch_sales_data(item, timeframe)

    if not data:
        messagebox.showinfo("No Data", f"No sales data found for {item} ({timeframe})")
        return

    dates, quantities = zip(*data)

    # Create the figure and plot the data
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(dates, quantities, marker="o", linestyle="-", color="b", label=item)
    ax.set_title(f"Sales Trend for {item} ({timeframe})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Quantity Sold")
    ax.legend()
    ax.grid()

    # Show the graph in a new Tkinter window
    trend_window = tk.Toplevel()
    trend_window.title(f"Sales Trend: {item} ({timeframe})")

    canvas = FigureCanvasTkAgg(fig, master=trend_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Function to open the sales trend window
def open_sales_trend_window():
    trend_window = tk.Toplevel()
    trend_window.title("Generate Sales Trends")
    trend_window.geometry("400x300")

    tk.Label(trend_window, text="Select Item:", font=("Arial", 12)).pack(pady=5)
    item_var = tk.StringVar()
    item_dropdown = ttk.Combobox(trend_window, textvariable=item_var, values=get_items(), state="readonly")
    item_dropdown.pack(pady=5)

    tk.Label(trend_window, text="Select Timeframe:", font=("Arial", 12)).pack(pady=5)
    timeframe_var = tk.StringVar(value="Daily")
    timeframe_dropdown = ttk.Combobox(trend_window, textvariable=timeframe_var, values=["Daily", "Weekly", "Monthly"], state="readonly")
    timeframe_dropdown.pack(pady=5)

    generate_btn = tk.Button(trend_window, text="Generate Trend", font=("Arial", 12), command=lambda: plot_sales_trend(item_var.get(), timeframe_var.get()))
    generate_btn.pack(pady=20)

# Show sales trend

def generate_sales_trends():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Fetch sales data
    cursor.execute("SELECT date_sold, price FROM sales")
    sales_data = cursor.fetchall()
    conn.close()

    if not sales_data:
        messagebox.showinfo("No Data", "No sales data available to generate trends.")
        return

    # Convert data into a DataFrame for easy manipulation
    df = pd.DataFrame(sales_data, columns=["date_sold", "price"])
    df["date_sold"] = pd.to_datetime(df["date_sold"])  # Convert to datetime

    # Group sales data for trends
    daily_sales = df.groupby(df["date_sold"].dt.date)["price"].sum()
    weekly_sales = df.groupby(df["date_sold"].dt.to_period("W"))["price"].sum()
    monthly_sales = df.groupby(df["date_sold"].dt.to_period("M"))["price"].sum()

    # Plot sales trends
    plt.figure(figsize=(12, 6))

    plt.subplot(3, 1, 1)
    plt.plot(daily_sales.index, daily_sales.values, marker="o", linestyle="-", color="b")
    plt.title("Daily Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)

    plt.subplot(3, 1, 2)
    plt.plot(weekly_sales.index.astype(str), weekly_sales.values, marker="o", linestyle="-", color="g")
    plt.title("Weekly Sales Trend")
    plt.xlabel("Week")
    plt.ylabel("Total Sales")

    plt.subplot(3, 1, 3)
    plt.plot(monthly_sales.index.astype(str), monthly_sales.values, marker="o", linestyle="-", color="r")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")

    plt.tight_layout()
    plt.show()

# Check Expection Reports

def view_exception_reports():
    report_window = tk.Toplevel()
    report_window.title("Exception Reports")
    report_window.geometry("600x400")

    tk.Label(report_window, text="Reported Exception Issues", font=("Arial", 14)).pack(pady=10)

    report_list = tk.Listbox(report_window, font=("Arial", 12), width=80, height=15)
    report_list.pack(pady=10)

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, item_name, issue FROM exception_reports WHERE resolved = 0")
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
        cursor.execute("UPDATE exception_reports SET resolved = 1 WHERE id=?", (report_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Report marked as resolved!")
        report_list.delete(selected[0])  # Remove from listbox

    tk.Button(report_window, text="Mark as Resolved", font=("Arial", 12), command=mark_resolved).pack(pady=10)