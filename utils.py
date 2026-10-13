import re
from datetime import datetime


class InvalidInputError(Exception):
    pass


def validate_date(date_text):
    pattern = r"^\d{4}-\d{2}-\d{2}$"

    if not re.fullmatch(pattern, date_text):
        return False

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_expense_id(expense_id):
    pattern = r"EXP-[0-9]{3}"
    return re.fullmatch(pattern, expense_id) is not None


def generate_expense_id(expenses):
    largest_id = 0

    for expense in expenses:
        if validate_expense_id(expense.expense_id):
            number = int(expense.expense_id[4:])
            largest_id = max(largest_id, number)

    return f"EXP-{largest_id + 1:03d}"


def parse_tags(tag_text):
    tags = set()

    for tag in tag_text.split(","):
        cleaned_tag = tag.strip().lower()

        if cleaned_tag:
            tags.add(cleaned_tag)

    return tags