import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity_sold INTEGER NOT NULL,
        date_sold TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("Sales table created successfully!")

# conn = sqlite3.connect("inventory.db")
# cursor = conn.cursor()

#     # SQL command to drop the sales table
# cursor.execute("DROP TABLE IF EXISTS sales")

# conn.commit()
# conn.close()
# print("✅ 'sales' table deleted successfully.")