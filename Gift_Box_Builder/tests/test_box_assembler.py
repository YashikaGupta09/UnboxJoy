"""Unit tests for GiftBox and SmartBoxAssembler."""

import unittest
from Gift_Box_Builder.backend.models import Product
from Gift_Box_Builder.backend.box_assembler import GiftBox, SmartBoxAssembler


class TestBoxAssembler(unittest.TestCase):

    def setUp(self):
        self.products = [
            Product("SIGHT001", "Photo Frame", "Chumbak", "sight", 300.0, match_score=0.9),
            Product("SOUND001", "Mini Speaker", "Mivi", "sound", 400.0, match_score=0.85),
            Product("SMELL001", "Lavender Candle", "Ekam", "smell", 250.0, match_score=0.95),
            Product("TASTE001", "Dark Chocolate", "Fabelle", "taste", 200.0, match_score=0.88),
            Product("TOUCH001", "Notebook", "Factor Notes", "touch", 150.0, match_score=0.82),
            Product("SIGHT002", "Wall Art", "Chumbak", "sight", 500.0, match_score=0.7)  # Same brand as SIGHT001
        ]

    def test_add_and_remove_item(self):
        box = GiftBox(target_budget=2000.0)
        success, msg = box.add_item(self.products[0])
        self.assertTrue(success)
        self.assertEqual(len(box.items), 1)

        # Duplicate check
        dup_success, dup_msg = box.add_item(self.products[0])
        self.assertFalse(dup_success)
        self.assertIn("already in the box", dup_msg)

        # Remove check
        rem_success, rem_msg = box.remove_item(self.products[0].product_id)
        self.assertTrue(rem_success)
        self.assertEqual(len(box.items), 0)

    def test_strict_budget_rejection(self):
        box = GiftBox(target_budget=350.0, packaging_id="eco_kraft")
        # Packaging is 99. Adding product of 300 makes taxable 399 + GST > 350
        success, msg = box.add_item(self.products[0], strict_budget=True)
        self.assertFalse(success)
        self.assertIn("exceeds your", msg)

    def test_auto_assemble_optimizer(self):
        # Budget = 1500
        box, msg = SmartBoxAssembler.auto_assemble(
            candidate_products=self.products,
            target_budget=1500.0,
            packaging_id="eco_kraft",
            target_item_count=4
        )
        self.assertIsNotNone(box)
        self.assertGreaterEqual(len(box.items), 3)

        pricing = box.get_pricing()
        self.assertFalse(pricing.budget_exceeded)
        self.assertLessEqual(pricing.grand_total, 1500.0)

        # Brand diversity check: no duplicate brands in assembled box
        brands = [item.brand for item in box.items]
        self.assertEqual(len(brands), len(set(brands)), "Assembled box contains duplicate brands")


if __name__ == "__main__":
    unittest.main()
