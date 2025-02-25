import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("💰 Smart Expense Tracker - CSV Sample Data")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "View Data", "Analysis"])

@st.cache  # Cache the result to avoid reloading on every interaction
def load_data():
    # Load sample data from the CSV file named "money spend.csv"
    df = pd.read_csv("money spend.csv")
    return df

# Load data from CSV
expense_data = load_data()

# Home Page
if page == "Home":
    st.write("### Welcome!")
    st.write("This app uses predefined expense data from the CSV file 'money spend.csv'.")

# View Data Page
elif page == "View Data":
    st.write("### Expense Data")
    st.dataframe(expense_data)

# Analysis Page
elif page == "Analysis":
    st.write("### Expense Analysis")
    if not expense_data.empty:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x="category", y="amount", data=expense_data, ax=ax)
        ax.set_title("Expense Distribution by Category")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No data available for analysis.")
