import sqlite3
import pandas as pd

# Function to establish a database connection
def get_connection():
    conn = sqlite3.connect("expenses.db", check_same_thread=False)
    return conn

# Create table if it doesn't exist
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

# Initialize the database on import
initialize_database()

# Function to add an expense
def add_expense(date, category, amount, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)", 
                       (str(date), category, float(amount), description))
        conn.commit()
        print("✅ Expense added successfully!")  # Debugging
    except Exception as e:
        print(f"❌ Error: {e}")  # Debugging
    finally:
        conn.close()

# Function to get all expenses
def get_expenses():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()
    return df
