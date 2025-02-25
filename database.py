import sqlite3
import pandas as pd
import os

# Define the database file path relative to this file
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
print("Database path:", os.path.abspath(DATABASE_PATH))  # Debug: show absolute path

def get_connection():
    return sqlite3.connect(DATABASE_PATH, check_same_thread=False)

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

# Create table on startup
initialize_database()

def add_expense(date, category, amount, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
            (str(date), category, float(amount), description)
        )
        conn.commit()
        print("✅ Expense added successfully!")
    except Exception as e:
        print("❌ Error adding expense:", e)
    finally:
        conn.close()

def get_expenses():
    conn = get_connection()
    try:
        df = pd.read_sql("SELECT * FROM expenses", conn)
    except Exception as e:
        print("❌ Error fetching expenses:", e)
        df = pd.DataFrame()
    finally:
        conn.close()
    return df
