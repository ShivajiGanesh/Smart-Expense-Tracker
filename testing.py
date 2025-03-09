import database  # Import the database module
import analysis  # Import the analysis module

def test_database():
    print("\U0001F50D Testing Database Functions...")  # 🔍
    
    # Add test expenses
    database.add_expense("Lunch", 150, "Food")
    database.add_expense("Transport", 50, "Travel")
    database.add_expense("Groceries", 500, "Shopping")
    
    # Retrieve expenses
    expenses = database.get_expenses()
    print("\u2705 Expenses Retrieved:\n", expenses)  # ✅

    # Delete an expense (assumes deletion by ID)
    if not expenses.empty:
        expense_id = expenses.iloc[0]["id"]
        database.delete_expense(expense_id)
        print(f"\U0001F5D1 Deleted Expense ID: {expense_id}")  # 🗑

    # Check expenses after deletion
    updated_expenses = database.get_expenses()
    print("\U0001F4CC Updated Expenses:\n", updated_expenses)  # 📌

def test_analysis():
    print("\U0001F4CA Testing Analysis Functions...")  # 📊
    
    # Generate and show a bar chart
    analysis.plot_expense_distribution()

if __name__ == "__main__":
    test_database()
    test_analysis()
    print("\u2705 All tests completed successfully!")  # ✅
