import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import database  # Import database functions from database.py

# ---- Streamlit UI ----
st.title("💰 Smart Expense Tracker")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add Expense", "View Expenses", "Analysis"])

# ---- Home Page ----
if page == "Home":
    st.write("### Welcome to Smart Expense Tracker!")
    st.write("Use this app to track your expenses efficiently.")

# ---- Add Expense ----
elif page == "Add Expense":
    st.subheader("📝 Add a New Expense")
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    amount = st.number_input("Amount (₹)", min_value=1.0)
    description = st.text_area("Description")

    if st.button("Add Expense"):
        database.add_expense(date, category, amount, description)  # Call function from database.py
        st.success("Expense added successfully!")

# ---- View Expenses ----
elif page == "View Expenses":
    st.subheader("📄 Your Expenses")
    df = database.get_expenses()  # Retrieve data from database.py
    st.dataframe(df)

# ---- Analysis ----
elif page == "Analysis":
    st.subheader("📊 Expense Analysis")
    
    df = database.get_expenses()
    if not df.empty:
        fig, ax = plt.subplots()
        sns.barplot(x="category", y="amount", data=df, ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No data available for analysis.")

# ---- Run Streamlit App ----
if __name__ == "__main__":
    st.write("Run this file using `streamlit run App.py`")
