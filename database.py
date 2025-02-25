import sqlite3
import pandas as pd

# Function to get a persistent database connection
def get_connection():
    return sqlite3.connect("expenses.db", check_same_thread=False)

# Ensure table is created on startup
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

# Initialize the database
initialize_database()

# Function to add an expense
def add_expense(date, category, amount, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)", 
                       (str(date), category, float(amount), description))
        conn.commit()
        print("✅ Expense added successfully!")  # Debugging message
    except Exception as e:
        print(f"❌ Error adding expense: {e}")  # Debugging message
    finally:
        conn.close()

# Function to get all expenses
def get_expenses():
    conn = get_connection()
    try:
        df = pd.read_sql("SELECT * FROM expenses", conn)  # Fetch data
    except Exception as e:
        print(f"❌ Error fetching expenses: {e}")  # Debugging message
        df = pd.DataFrame()  # Return an empty DataFrame if error occurs
    finally:
        conn.close()
    return df
