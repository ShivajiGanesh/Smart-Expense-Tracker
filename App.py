import streamlit as st
import pandas as pd
import os

# CSV file path
CSV_FILE = "expenses.csv"

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(CSV_FILE, index=False)

st.title("💰 Smart Expense Tracker - CSV Based")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add Expense", "View Expenses", "Analysis"])

# Function to load data from CSV
@st.cache
def load_data():
    return pd.read_csv(CSV_FILE)

# Function to add an expense and update the CSV file
def add_expense(date, category, amount, description):
    df = pd.read_csv(CSV_FILE)
    new_expense = pd.DataFrame([[date, category, amount, description]], 
                               columns=["Date", "Category", "Amount", "Description"])
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.success("Expense added successfully!")

# Home Page
if page == "Home":
    st.write("### Welcome!")
    st.write("Track your expenses and analyze them with this CSV-based system.")

# Add Expense Page
elif page == "Add Expense":
    st.subheader("📝 Add a New Expense")
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    amount = st.number_input("Amount (₹)", min_value=1.0)
    description = st.text_area("Description")

    if st.button("Add Expense"):
        add_expense(date, category, amount, description)

# View Expenses Page
elif page == "View Expenses":
    st.subheader("📄 Your Expenses")
    df = load_data()
    st.dataframe(df)

# Analysis Page
elif page == "Analysis":
    st.subheader("📊 Expense Analysis")
    df = load_data()

    if not df.empty:
        st.bar_chart(df.groupby("Category")["Amount"].sum())
    else:
        st.warning("No data available for analysis.")
