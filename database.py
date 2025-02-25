import sqlite3
import pandas as pd

# Function to establish a database connection
def get_connection():
    return sqlite3.connect("expenses.db")

# Create Table if not exists
conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT
    )
""")
conn.commit()
conn.close()  # Close after creation

# Function to add expense
def add_expense(date, category, amount, description):
    print(f"Trying to add: {date}, {category}, {amount}, {description}")  # Debugging
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)", 
                   (date, category, amount, description))
    conn.commit()
    conn.close()
    print("Expense added successfully!")

# Function to get all expenses
def get_expenses():
    conn = get_connection()  # Open new connection here
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()
    return df
