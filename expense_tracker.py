import sqlite3
import matplotlib.pyplot as plt

# Connect to database
connection = sqlite3.connect("expenses.db")
cursor = connection.cursor()

# Create expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
)
""")

connection.commit()


# Add expense
def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    description = input("Enter description: ")
    date = input("Enter date (YYYY-MM-DD): ")

    cursor.execute("""
    INSERT INTO expenses (amount, category, description, date)
    VALUES (?, ?, ?, ?)
    """, (amount, category, description, date))

    connection.commit()
    print("Expense added successfully!")


# View expenses
def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses found.")
    else:
        for expense in expenses:
            print(expense)


# Delete expense
def delete_expense():
    expense_id = int(input("Enter expense ID to delete: "))

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    connection.commit()

    print("Expense deleted successfully!")


# Total spending
def total_spending():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print("\nTotal Spending:", total)


# Category-wise spending
def category_spending():
    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    """)

    category_totals = cursor.fetchall()

    print("\n--- Category-wise Spending ---")

    if not category_totals:
        print("No expenses found.")
    else:
        for category, total in category_totals:
            print(category, ":", total)


# Spending chart
def spending_chart():
    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    """)

    category_totals = cursor.fetchall()

    if not category_totals:
        print("No expenses available for chart.")
        return

    categories = [item[0] for item in category_totals]
    amounts = [item[1] for item in category_totals]

    plt.bar(categories, amounts)
    plt.xlabel("Category")
    plt.ylabel("Amount Spent")
    plt.title("Expense Spending by Category")
    plt.show()


# Main menu
while True:
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Total Spending")
    print("5. Category-wise Spending")
    print("6. Spending Chart")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        delete_expense()

    elif choice == "4":
        total_spending()

    elif choice == "5":
        category_spending()

    elif choice == "6":
        spending_chart()

    elif choice == "7":
        print("Thank you for using Expense Tracker!")
        break

    else:
        print("Invalid choice. Please try again.")


connection.close()