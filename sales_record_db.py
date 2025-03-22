import sqlite3

# Connect to the inventory database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create sales_records table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    quantity_sold INTEGER NOT NULL,
    sale_date DATE NOT NULL
);
""")

# Commit and close the connection
conn.commit()
conn.close()

print("sales_records table created successfully.")

