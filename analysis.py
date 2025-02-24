import matplotlib.pyplot as plt
import seaborn as sns
import database  # Import database functions

def plot_expense_distribution():
    expenses = database.get_expenses()  # Fetch expenses from database.py
    
    if expenses.empty:  # Correct way to check if DataFrame is empty
        print("No data available for visualization.")
        return

    plt.figure(figsize=(8, 5))
    sns.barplot(x="category", y="amount", data=expenses)
    plt.title("Expense Distribution by Category")
    plt.xticks(rotation=45)
    plt.show()

# Testing visualization
if __name__ == "__main__":
    plot_expense_distribution()
