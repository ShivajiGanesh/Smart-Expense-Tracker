import sqlite3
import pandas as pd

# Database Connection
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create Table if not exists
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

# Function to add expense
def add_expense(date, category, amount, description):
    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)", 
                   (date, category, amount, description))
    conn.commit()
    print("\u2705 Expense added successfully!")

# Function to get all expenses
def get_expenses():
    df = pd.read_sql("SELECT * FROM expenses", conn)
    return df
