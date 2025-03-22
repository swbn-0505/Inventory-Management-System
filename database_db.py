import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Creating Inventory Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
)
''')

conn.commit()
conn.close()

print("Inventory Table Created Successfully!")

