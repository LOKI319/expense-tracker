import unittest
import os
from expense_tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_expenses.json"
        self.tracker = ExpenseTracker(file_path=self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_expense(self):
        self.tracker.add_expense(100, "Food", "Lunch")
        expenses = self.tracker.view_expenses()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["amount"], 100)

    def test_summary_by_month(self):
        self.tracker.add_expense(50, "Travel", "Bus fare", "2025-08-20")
        self.tracker.add_expense(150, "Food", "Dinner", "2025-08-20")
        summary = self.tracker.get_summary(by="month")
        self.assertIn("2025-08", summary)
        self.assertEqual(summary["2025-08"], 200)

    def test_summary_by_category(self):
        self.tracker.add_expense(200, "Utilities", "Electricity")
        self.tracker.add_expense(100, "Utilities", "Water")
        summary = self.tracker.get_summary(by="category")
        self.assertEqual(summary["Utilities"], 300)


if __name__ == "__main__":
    unittest.main()
