import matplotlib.pyplot as plt
import seaborn as sns
import database

def plot_expense_distribution():
    # Fetch all expenses from the database.
    df = database.get_expenses()
    if df.empty:
        print("No data available for analysis.")
        return None

    # Create a figure for the bar plot.
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="category", y="amount", data=df, ax=ax)
    ax.set_title("Expense Distribution by Category")
    # Rotate category labels for better readability.
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# If you run analysis.py directly, display the plot.
if __name__ == "__main__":
    fig = plot_expense_distribution()
    if fig:
        plt.show()
