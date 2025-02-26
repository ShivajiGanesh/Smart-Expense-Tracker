import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

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
page = st.sidebar.radio("Go to", ["Home", "Add Expense", "View Expenses", "Analysis", "Budget & Insights"])

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
        
        # Add Download CSV Button
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV", 
            data=csv_data, 
            file_name="expenses.csv", 
            mime="text/csv"
        )
    
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
        # Ensure 'Date' is in datetime format and sort data
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")

        # Create a figure and axis with a specific size
        fig, ax = plt.subplots(figsize=(10, 6))

        # Set a slightly darker grey background for visibility
        ax.set_facecolor("#c0c0c0")  # Medium grey background
        fig.patch.set_facecolor("#ffffff")  # White background for the figure

        # Plot connected scatterplot
        ax.plot(df["Date"], df["Amount"], linestyle="-", color="#002147",  # Dark blue line
                linewidth=2, alpha=0.9)  

        # Scatter plot for individual data points
        ax.scatter(df["Date"], df["Amount"], color="#ff6700", edgecolor="black",  # Orange dots with black edge
                   s=80, zorder=3)  # Size increased for better visibility

        # Annotate each point
        for i, row in df.iterrows():
            ax.text(row["Date"], row["Amount"], f"₹{row['Amount']:.0f}",
                    fontsize=9, verticalalignment='bottom', color="black", fontweight="bold")

        # Set labels and title
        ax.set_xlabel("Date", fontsize=12, color="black", fontweight="bold")
        ax.set_ylabel("Amount Spent (₹)", fontsize=12, color="black", fontweight="bold")
        ax.set_title("📈 Spending Trend Analysis", fontsize=15, fontweight="bold", color="black")

        # Customize grid lines
        ax.grid(color='#8c8c8c', linestyle='--', linewidth=0.7, alpha=0.7)  

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, color="black")
        plt.yticks(color="black")

        # Display the plot
        st.pyplot(fig)
    else:
        st.warning("🚨 No data available for analysis.")



# Budget & Insights Page
elif page == "Budget & Insights":
    st.subheader("📈 Budget & Smart Insights")
    df = load_data()
    
    if df.empty:
        st.warning("🚨 No expenses recorded yet.")
    else:
        total_spent = df["Amount"].sum()
        avg_monthly_spend = total_spent / max(len(pd.to_datetime(df["Date"]).dt.to_period("M").unique()), 1)
        budget = avg_monthly_spend * 1.2  # Dynamic budget based on spending pattern
        
        st.write(f"📊 Your estimated budget: ₹{budget:.2f}")
        st.write(f"💰 Total spent so far: ₹{total_spent:.2f}")
        
        insights = []
        if total_spent > budget:
            insights.append("⚠️ You've exceeded your budget! Consider reducing expenses.")
        if total_spent > budget * 0.8:
            insights.append("🚨 You've spent 80% of your budget. Slow down on expenses!")
        
        category_spending = df.groupby("Category")["Amount"].sum()
        for category, amount in category_spending.items():
            if category == "Food" and amount > total_spent * 0.5:
                insights.append("🍔 You're spending a lot on Food! Consider meal planning to save money.")
            if category == "Transport" and amount > total_spent * 0.3:
                insights.append("🚗 High transport costs! Try public transport or carpooling.")
            if category == "Shopping" and amount > total_spent * 0.3:
                insights.append("🛍️ Excessive shopping detected! Set a shopping limit to avoid overspending.")
        
        st.write("\n".join(insights) if insights else "✅ Your spending is well-balanced!")
