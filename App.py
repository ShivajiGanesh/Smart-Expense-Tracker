import streamlit as st
import pandas as pd
import os

# Define the directory and CSV file path
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "expenses.csv")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Ensure CSV file exists with proper headers
if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(CSV_FILE, index=False)

st.title("💰 Smart Expense Tracker - CSV Based")

# Show CSV path for debugging
st.sidebar.write(f"📁 CSV Path: `{CSV_FILE}`")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add Expense", "View Expenses", "Analysis"])

# Function to load data (forces refresh)
def load_data():
    return pd.read_csv(CSV_FILE)

# Function to add an expense and update CSV
def add_expense(date, category, amount, description):
    df = pd.DataFrame([[date, category, amount, description]], 
                      columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(CSV_FILE, mode='a', index=False, header=False)  # Append data
    st.success("✅ Expense added successfully!")

# Home Page
if page == "Home":
    st.write("### Welcome to the Smart Expense Tracker!")
    st.write("Track and analyze your expenses with this simple CSV-based app.")

# Add Expense Page
elif page == "Add Expense":
    st.subheader("📝 Add a New Expense")
    date = st.date_input("📅 Date")
    category = st.selectbox("📂 Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    amount = st.number_input("💰 Amount (₹)", min_value=1.0)
    description = st.text_area("📝 Description")

    if st.button("➕ Add Expense"):
        add_expense(date, category, amount, description)

# View Expenses Page
elif page == "View Expenses":
    st.subheader("📄 Your Expenses")
    df = load_data()
    if df.empty:
        st.warning("🚨 No expenses recorded yet.")
    else:
        st.dataframe(df)
    # Add a reset button
    if st.button("🗑 Reset All Expenses"):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(CSV_FILE, index=False)
        st.warning("🚨 All expenses have been cleared!")

# Analysis Page
elif page == "Analysis":
    st.subheader("📊 Expense Analysis")
    df = load_data()
    
    if not df.empty:
        st.bar_chart(df.groupby("Category")["Amount"].sum())
    else:
        st.warning("🚨 No data available for analysis.")
