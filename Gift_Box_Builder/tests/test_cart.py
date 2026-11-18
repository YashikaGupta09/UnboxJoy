"""Unit tests for CartManager and Order Receipt generation."""

import unittest
from Gift_Box_Builder.backend.models import Product
from Gift_Box_Builder.backend.box_assembler import GiftBox
from Gift_Box_Builder.backend.cart import CartManager


class TestCartManager(unittest.TestCase):

    def setUp(self):
        self.box = GiftBox(target_budget=2000.0)
        self.box.add_item(Product("SIGHT001", "Photo Frame", "Chumbak", "sight", 300.0))
        self.box.add_item(Product("SMELL001", "Lavender Candle", "Ekam", "smell", 250.0))
        self.box.add_item(Product("TASTE001", "Dark Chocolate", "Fabelle", "taste", 200.0))

    def test_order_summary_generation(self):
        summary = CartManager.generate_order_summary(
            box=self.box,
            recipient_name="Aarav",
            sender_name="Pooja",
            occasion="Graduation",
            personalized_message="So proud of you! Here are some little joys."
        )

        self.assertEqual(summary["status"], "confirmed")
        self.assertTrue(summary["order_id"].startswith("UBJ-"))
        self.assertEqual(summary["recipient_details"]["name"], "Aarav")
        self.assertEqual(summary["item_count"], 3)
        self.assertIn("financial_summary", summary)
        self.assertIn("unboxing_experience", summary)
        self.assertEqual(len(summary["unboxing_experience"]["reveal_sequence"]), 3)

    def test_empty_box_checkout_rejection(self):
        empty_box = GiftBox(target_budget=1000.0)
        with self.assertRaises(ValueError):
            CartManager.generate_order_summary(empty_box)


if __name__ == "__main__":
    unittest.main()
