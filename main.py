from models import Expense, ExpenseTracker
from storage import save_to_json, load_from_json
from utils import validate_date, generate_expense_id, parse_tags


FILENAME = "expenses.json"


def show_budget_status(tracker):
    total = tracker.get_total_spending()
    budget = tracker.budget_limit

    if total > budget:
        print("Warning: You have exceeded your budget!")
    elif budget > 0 and total >= budget * 0.8:
        print("Warning: You have used at least 80% of your budget.")
    else:
        print("Your spending is within the budget.")

    print(f"Total spending: ₹{total:.2f}")
    print(f"Budget limit: ₹{budget:.2f}")


def add_expense(tracker):
    print("\n--- Add Expense ---")

    date = input("Enter date (YYYY-MM-DD): ").strip()

    if not validate_date(date):
        print("Invalid date. Please use a real date in YYYY-MM-DD format.")
        return

    category = input("Enter category: ").strip().title()

    if not category:
        print("Category cannot be empty.")
        return

    try:
        amount = float(input("Enter amount: ₹").strip())

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    tag_text = input("Enter tags separated by commas: ")
    tags = parse_tags(tag_text)

    expense_id = generate_expense_id(tracker.expenses)

    expense = Expense(
        expense_id,
        date,
        category,
        amount,
        tags
    )

    tracker.add_expense(expense)

    print("\nExpense added successfully!")
    print(expense)

    show_budget_status(tracker)


def view_expenses(tracker):
    print("\n--- All Expenses ---")

    if not tracker.expenses:
        print("No expenses recorded yet.")
        return

    print(
        f"{'ID':<10} {'Date':<12} "
        f"{'Category':<15} {'Amount':>10} {'Tags'}"
    )
    print("-" * 65)

    for expense in tracker.expenses:
        tags = ", ".join(sorted(expense.tags))

        print(
            f"{expense.expense_id:<10} "
            f"{expense.date:<12} "
            f"{expense.category:<15} "
            f"₹{expense.amount:>9.2f} {tags}"
        )

    count, total = tracker.get_summary()

    print("-" * 65)
    print(f"Number of expenses: {count}")
    print(f"Total spending: ₹{total:.2f}")


def view_category_summary(tracker):
    print("\n--- Category Summary ---")

    summary = tracker.category_summary()

    if not summary:
        print("No expenses recorded yet.")
        return

    for category, amount in summary.items():
        print(f"{category}: ₹{amount:.2f}")

    print(f"Total spending: ₹{tracker.get_total_spending():.2f}")


def search_by_category(tracker):
    print("\n--- Search by Category ---")

    category = input("Enter category to search: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    results = tracker.filter_by_category(category)

    if not results:
        print("No expenses found for this category.")
        return

    for expense in results:
        print(expense)


def main():
    expenses = load_from_json(FILENAME)

    try:
        budget = float(input("Enter your total budget (₹): "))

        if budget < 0:
            print("Budget cannot be negative.")
            return

    except ValueError:
        print("Invalid budget. Please enter a number.")
        return

    tracker = ExpenseTracker(expenses, budget)

    print("\nWelcome to SpendWise CLI!")

    while True:
        print("\n========== SPENDWISE EXPENSE TRACKER ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Category Summary")
        print("4. Search Expenses by Category")
        print("5. Save and Exit")

        choice = input("Enter your choice: ").strip()

        match choice:
            case "1":
                add_expense(tracker)

            case "2":
                view_expenses(tracker)

            case "3":
                view_category_summary(tracker)

            case "4":
                search_by_category(tracker)

            case "5":
                try:
                    save_to_json(FILENAME, tracker.expenses)
                    print("Expenses saved successfully.")
                    print("Thank you for using SpendWise!")
                except OSError as error:
                    print(f"Could not save expenses: {error}")

                break

            case _:
                print("Invalid option! Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()