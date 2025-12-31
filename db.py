import sqlite3
import os

# Ensure the examples directory exists
os.makedirs("examples", exist_ok=True)

# Connect to SQLite database (this creates the file if it doesn't exist)
conn = sqlite3.connect('examples/db.sqlite')
cursor = conn.cursor()

# SQL statements
sql_script = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
"""

# Execute the script
try:
    cursor.executescript(sql_script)
    print("Database created successfully at examples/db.sqlite")
    print("Tables 'customers' and 'orders' initialized.")
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    conn.commit()
    conn.close()
