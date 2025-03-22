import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

###CREATE THE TABLE

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS sales_reports (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         item_name TEXT NOT NULL,
#         issue TEXT NOT NULL,
#         reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
# """)

# conn.commit()
# conn.close()

### ADD Issue COLUMNS

# # Add the missing column
# cursor.execute("ALTER TABLE sales_reports ADD COLUMN issue TEXT")

# conn.commit()
# conn.close()
# print("Column 'issue' added successfully!")

## ADD resolved COLUMNS

# Add the missing column
cursor.execute("ALTER TABLE sales_reports ADD COLUMN resolved INTEGER")

conn.commit()
conn.close()
print("Column 'resolved' added successfully!")


### UNCOMMENT ABOVE CODE TO ADD TABLE