import json
from datetime import datetime
from typing import List, Dict


class Expense:
    def __init__(self, amount: float, category: str, description: str, date: str = None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self) -> Dict:
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }


class ExpenseTracker:
    def __init__(self, file_path="expenses.json"):
        self.file_path = file_path
        self.expenses = self._load_expenses()

    def _load_expenses(self) -> List[Dict]:
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_expenses(self):
        with open(self.file_path, "w") as f:
            json.dump(self.expenses, f, indent=4)

    def add_expense(self, amount: float, category: str, description: str, date: str = None):
        expense = Expense(amount, category, description, date)
        self.expenses.append(expense.to_dict())
        self._save_expenses()

    def view_expenses(self) -> List[Dict]:
        return self.expenses

    def get_summary(self, by: str = "month") -> Dict:
        summary = {}
        for exp in self.expenses:
            key = None
            if by == "month":
                key = exp["date"][:7]  # YYYY-MM
            elif by == "day":
                key = exp["date"]
            elif by == "category":
                key = exp["category"]

            if key not in summary:
                summary[key] = 0
            summary[key] += exp["amount"]

        return summary


# Example CLI usage
if __name__ == "__main__":
    tracker = ExpenseTracker()

    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Summary (by month)")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description: ")
            tracker.add_expense(amount, category, description)
            print("✅ Expense added!")
        elif choice == "2":
            for exp in tracker.view_expenses():
                print(exp)
        elif choice == "3":
            summary = tracker.get_summary(by="month")
            print("📊 Monthly Summary:", summary)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")
