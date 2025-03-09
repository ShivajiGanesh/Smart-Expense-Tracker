import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator

# Define the directory and CSV file path
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "expenses.csv")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Ensure CSV file exists with proper headers
if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(CSV_FILE, index=False)

st.title("\U0001F4B0 Smart Expense Tracker - CSV Based")

# Show CSV path for debugging
st.sidebar.write(f"\U0001F4C1 CSV Path: `{CSV_FILE}`")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add Expense", "View Expenses", "Analysis", "Budget & Insights"])

# Function to load data (forces refresh)
def load_data():
    return pd.read_csv(CSV_FILE)

# Function to add an expense and update CSV
def add_expense(date, category, amount, description):
    df = pd.DataFrame([[date, category, amount, description]], 
                      columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(CSV_FILE, mode='a', index=False, header=False)  # Append data
    st.success("\U00002705 Expense added successfully!")

# Home Page
if page == "Home":
    st.write("### Welcome to the Smart Expense Tracker!")
    st.write("Track and analyze your expenses with this simple CSV-based app.")

# Add Expense Page
elif page == "Add Expense":
    st.subheader("\U0001F4DD Add a New Expense")
    date = st.date_input("\U0001F4C5 Date")
    category = st.selectbox("\U0001F4C2 Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    amount = st.number_input("\U0001F4B0 Amount (₹)", min_value=1.0)
    description = st.text_area("\U0001F4DD Description")

    if st.button("\U00002795 Add Expense"):
        add_expense(date, category, amount, description)

# View Expenses Page
elif page == "View Expenses":
    st.subheader("\U0001F4C4 Your Expenses")
    df = load_data()
    if df.empty:
        st.warning("\U0001F6A8 No expenses recorded yet.")
    else:
        st.dataframe(df)
        
        # Add Download CSV Button
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="\U0001F4E5 Download CSV", 
            data=csv_data, 
            file_name="expenses.csv", 
            mime="text/csv"
        )
    
    # Add a reset button
    if st.button("\U0001F5D1 Reset All Expenses"):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(CSV_FILE, index=False)
        st.warning("\U0001F6A8 All expenses have been cleared!")

# Analysis Page
elif page == "Analysis":
    st.subheader("\U0001F4CA Expense Analysis")
    df = load_data()
    
    if not df.empty:
        # Convert Date column to datetime format
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
        df = df.dropna(subset=["Date"])  # Remove invalid dates
        df = df.sort_values("Date")

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")  # White outer background
        ax.set_facecolor("#0d1b2a")  # Dark charcoal grey for inside graph

        # Plot data
        ax.plot(df["Date"], df["Amount"], marker='o', linestyle='-', color='#FF6700', 
                linewidth=2, markersize=6, markerfacecolor='#002147')  # Orange line & Dark Blue dots
        ax.grid(color="#555555", linestyle="--", linewidth=0.6)  # Medium grey grid

        # Add text labels for each data point
        for i, row in df.iterrows():
            ax.text(row["Date"], row["Amount"], f"₹{row['Amount']:.2f}", fontsize=9, 
                    color='white', verticalalignment='bottom')

        # Set labels and title
        ax.set_xlabel("Date", fontsize=12, color='black')
        ax.set_ylabel("Amount Spent (₹)", fontsize=12, color='black')
        ax.set_title("Spending Trend", fontsize=14, color='black')

        # Fix the x-axis date formatting
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))  # Format as YYYY-MM-DD
        ax.xaxis.set_major_locator(DayLocator(interval=1))  # Adjust interval for better readability

        plt.xticks(rotation=45, color='black')  # Rotate x-axis labels
        plt.yticks(color='black')

        # Show plot in Streamlit
        st.pyplot(fig)
    else:
        st.warning("\U0001F6A8 No data available for analysis.")

# Budget & Insights Page
elif page == "Budget & Insights":
    st.subheader("\U0001F4C8 Budget & Smart Insights")
    df = load_data()
    
    if df.empty:
        st.warning("\U0001F6A8 No expenses recorded yet.")
    else:
        salary = st.number_input("\U0001F4B5 Enter Your Monthly Salary (₹)", min_value=1000.0)
        daily_budget = salary / 30
        total_spent = df["Amount"].sum()
        estimated_budget = salary  # Full monthly salary as budget
        
        st.write(f"\U0001F4CA Your estimated monthly budget: ₹{estimated_budget:.2f}")
        st.write(f"\U0001F4B0 Total spent so far: ₹{total_spent:.2f}")
        
        insights = []
        percentage_spent = (total_spent / estimated_budget) * 100 if estimated_budget > 0 else 0
        
        if total_spent > estimated_budget:
            insights.append("\U000026A0 You've exceeded your budget! Consider reducing expenses.")
        elif percentage_spent > 80:
            insights.append("\U0001F6A8 You've spent 80% of your budget. Slow down on expenses!")
        elif percentage_spent < 50:
            insights.append("\U00002705 You're on track! Keep up the good spending habits.")
        
        st.write("\n".join(insights) if insights else "\U00002705 Your spending is well-balanced!")
