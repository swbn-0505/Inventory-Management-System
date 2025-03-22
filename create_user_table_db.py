import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        role TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")

# Commit and close connection
conn.commit()
conn.close()

print("Users table created successfully!")
