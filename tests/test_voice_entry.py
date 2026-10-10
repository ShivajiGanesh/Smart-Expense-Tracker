import unittest

from voice_entry import parse_expense_text


class ParseExpenseTextTests(unittest.TestCase):
    def test_mixed_telugu_english(self):
        draft = parse_expense_text("Ninna petrol ki 200 rupees pettanu")
        self.assertEqual(draft.amount, 200.0)
        self.assertEqual(draft.category, "Petrol / Fuel")

    def test_rupee_symbol_and_decimal_amount(self):
        draft = parse_expense_text("₹1,250.50 on petrol")
        self.assertEqual(draft.amount, 1250.50)
        self.assertEqual(draft.category, "Petrol / Fuel")

    def test_hindi_food_phrase(self):
        draft = parse_expense_text("आज खाने पर 250 रुपये खर्च किए")
        self.assertEqual(draft.amount, 250.0)
        self.assertEqual(draft.category, "Food / Groceries")

    def test_amount_without_category_needs_clarification(self):
        draft = parse_expense_text("spent 200 yesterday")
        self.assertEqual(draft.amount, 200.0)
        self.assertIsNone(draft.category)

    def test_category_without_amount_needs_clarification(self):
        draft = parse_expense_text("spent on petrol")
        self.assertIsNone(draft.amount)
        self.assertEqual(draft.category, "Petrol / Fuel")


if __name__ == "__main__":
    unittest.main()
