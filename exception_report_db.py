import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

##CREATE THE TABLE

cursor.execute("""
    CREATE TABLE IF NOT EXISTS exception_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        issue TEXT NOT NULL,
        reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved INTEGER
    )
""")

conn.commit()
conn.close()

print("Exception reports table created successfully")