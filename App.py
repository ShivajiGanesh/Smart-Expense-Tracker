import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# CSV file path
CSV_FILE = "expenses.csv"

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(CSV_FILE, index=False)

st.title("💰 Smart Expense Tracker - CSV Based")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add Expense", "View Expenses", "Analysis", "Budget & Insights"])

# Function to load data from CSV
@st.cache_data
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

# Function to analyze spending habits
def get_insights(df, budget):
    if df.empty:
        return "No expenses recorded yet."
    
    insights = []
    category_spending = df.groupby("Category")["Amount"].sum()
    total_spent = df["Amount"].sum()
    
    if total_spent > budget:
        insights.append("⚠️ You've exceeded your budget! Consider reducing expenses.")
    elif total_spent > budget * 0.8:
        insights.append("🚨 You've spent 80% of your budget. Slow down on expenses!")
    
    for category, amount in category_spending.items():
        if category == "Food" and amount > total_spent * 0.5:
            insights.append("🍔 You're spending a lot on Food! Consider meal planning to save money.")
        elif category == "Transport" and amount > total_spent * 0.3:
            insights.append("🚗 High transport costs! Try public transport or carpooling.")
        elif category == "Shopping" and amount > total_spent * 0.3:
            insights.append("🛍️ Excessive shopping detected! Set a shopping limit to avoid overspending.")
    
    return "\n".join(insights) if insights else "✅ Your spending is well-balanced!"

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
    if df.empty:
        st.warning("🚨 No expenses recorded yet.")
    else:
        st.dataframe(df)

    if st.button("🗑 Reset All Expenses"):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(CSV_FILE, index=False)
        st.warning("🚨 All expenses have been cleared!")

# Analysis Page
elif page == "Analysis":
    st.subheader("📊 Expense Analysis")
    df = load_data()

    if not df.empty:
        fig, ax = plt.subplots()
        sns.barplot(x="Category", y="Amount", data=df, ax=ax)
        st.pyplot(fig)
        
        st.subheader("📌 Category Breakdown")
        st.bar_chart(df.groupby("Category")["Amount"].sum())
    else:
        st.warning("No data available for analysis.")

# Budget & Insights Page
elif page == "Budget & Insights":
    st.subheader("📈 Budget & Smart Insights")
    budget = st.number_input("Set Monthly Budget (₹)", min_value=1000.0, value=5000.0)
    df = load_data()

    insights = get_insights(df, budget)
    st.write(insights)

    if not df.empty:
        st.subheader("📉 Monthly Spending Trend")
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
        st.line_chart(df.resample("M")["Amount"].sum())
