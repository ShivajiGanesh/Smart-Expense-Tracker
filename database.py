import sqlite3
import pandas as pd

# Use a persistent connection
DATABASE_FILE = "expenses.db"

def get_connection():
    return sqlite3.connect(DATABASE_FILE, check_same_thread=False)

# Ensure table exists
def initialize_database():
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
    conn.close()

initialize_database()  # Call on startup

# Add an expense
def add_expense(date, category, amount, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                       (str(date), category, float(amount), description))
        conn.commit()
        print("✅ Expense added successfully!")
    except Exception as e:
        print(f"❌ Error adding expense: {e}")
    finally:
        conn.close()

# Fetch all expenses
def get_expenses():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()
    return df
