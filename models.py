class Expense:
    def __init__(self, expense_id, date, category, amount, tags):
        self.expense_id = expense_id
        self.date = date
        self.category = category
        self.amount = amount
        self.tags = set(tags)

    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "tags": list(self.tags)
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["expense_id"],
            data["date"],
            data["category"],
            float(data["amount"]),
            data["tags"]
        )

    def __str__(self):
        tag_text = ", ".join(sorted(self.tags))
        return (
            f"[{self.date}] {self.category}: "
            f"₹{self.amount:.2f} (tags: {tag_text})"
        )


class ExpenseTracker:
    def __init__(self, expenses=None, budget_limit=0.0):
        self.expenses = expenses if expenses is not None else []
        self.budget_limit = float(budget_limit)

    def add_expense(self, expense):
        self.expenses.append(expense)

    def get_total_spending(self):
        total = 0.0

        for expense in self.expenses:
            total += expense.amount

        return total

    def is_over_budget(self):
        return self.get_total_spending() > self.budget_limit

    def category_summary(self):
        summary = {}

        for expense in self.expenses:
            category = expense.category
            summary[category] = (
                summary.get(category, 0.0) + expense.amount
            )

        return summary

    def filter_by_category(self, category_name):
        matching_expenses = []

        for expense in self.expenses:
            if expense.category.lower() == category_name.lower():
                matching_expenses.append(expense)

        return matching_expenses

    def sort_by_amount(self):
        return sorted(
            self.expenses,
            key=lambda expense: expense.amount,
            reverse=True
        )

    def get_summary(self):
        return len(self.expenses), self.get_total_spending()