import json

from models import Expense


def save_to_json(filename, expenses_list):
    data = []

    for expense in expenses_list:
        data.append(expense.to_dict())

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_from_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Warning: Expense file must contain a list.")
            return []

        expenses = []

        for item in data:
            expenses.append(Expense.from_dict(item))

        return expenses

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Warning: The JSON file is empty or corrupted.")
        return []

    except (ValueError, TypeError, KeyError) as error:
        print(f"Warning: Could not load expense records: {error}")
        return []