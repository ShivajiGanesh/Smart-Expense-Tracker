import database
import analysis

def test_add_expenses():
    print("=== Adding Test Expenses ===")
    # Add a few test expenses.
    database.add_expense("2025-02-25", "Food", 150, "Lunch")
    database.add_expense("2025-02-25", "Transport", 75, "Bus fare")
    database.add_expense("2025-02-25", "Shopping", 200, "Groceries")
    print("Test expenses added.\n")

def test_get_expenses():
    print("=== Fetching Expenses ===")
    df = database.get_expenses()
    if df.empty:
        print("No expenses found.")
    else:
        print("Expenses fetched successfully:")
        print(df)
    print()

def test_analysis_plot():
    print("=== Generating Analysis Plot ===")
    fig = analysis.plot_expense_distribution()
    if fig:
        # Optionally, save the figure to verify visually.
        fig.savefig("test_plot.png")
        print("Analysis plot generated and saved as 'test_plot.png'.")
    else:
        print("No data available for analysis plot.")
    print()

if __name__ == "__main__":
    test_add_expenses()
    test_get_expenses()
    test_analysis_plot()
    print("All tests completed successfully!")
