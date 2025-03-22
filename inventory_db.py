import sqlite3
import datetime

# Connect to the database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Step 1: Add the column WITHOUT default value
cursor.execute("ALTER TABLE inventory ADD COLUMN last_updated TIMESTAMP")

# Step 2: Set current timestamp for existing rows
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute("UPDATE inventory SET last_updated = ?", (current_time,))

# Commit and close
conn.commit()
conn.close()

print("Database updated! 'last_updated' column added and initialized.")
