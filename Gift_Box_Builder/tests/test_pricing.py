"""Unit tests for Person 4 domain models, packaging styles, and pricing engine."""

import unittest
from Gift_Box_Builder.backend.models import Product, GreetingCard
from Gift_Box_Builder.backend.packaging import get_all_packaging_options, get_packaging_by_id
from Gift_Box_Builder.backend.pricing import PricingEngine, SensoryCoverageEngine, GST_RATE


class TestModelsAndPricing(unittest.TestCase):

    def setUp(self):
        self.p1 = Product(
            product_id="SIGHT001",
            product_name="Chumbak Frame",
            brand="Chumbak",
            category="sight",
            price=500.0
        )
        self.p2 = Product(
            product_id="SOUND001",
            product_name="boAt Speaker",
            brand="boAt",
            category="sound",
            price=600.0
        )
        self.packaging = get_packaging_by_id("eco_kraft")

    def test_packaging_catalog(self):
        options = get_all_packaging_options()
        self.assertEqual(len(options), 4)
        ids = [opt.id for opt in options]
        self.assertIn("eco_kraft", ids)
        self.assertIn("midnight_luxe", ids)
        self.assertIn("pastel_blossom", ids)
        self.assertIn("velvet_chest", ids)

    def test_pricing_calculation_within_budget(self):
        pricing = PricingEngine.calculate([self.p1, self.p2], self.packaging, 1500.0)
        expected_subtotal = 1100.0
        expected_packaging = 99.0
        expected_tax = round((expected_subtotal + expected_packaging) * GST_RATE, 2)
        expected_total = expected_subtotal + expected_packaging + expected_tax

        self.assertEqual(pricing.items_subtotal, expected_subtotal)
        self.assertEqual(pricing.packaging_fee, expected_packaging)
        self.assertEqual(pricing.tax_gst, expected_tax)
        self.assertEqual(pricing.grand_total, expected_total)
        self.assertFalse(pricing.budget_exceeded)
        self.assertGreater(pricing.remaining_budget, 0)

    def test_pricing_budget_exceeded(self):
        pricing = PricingEngine.calculate([self.p1, self.p2], self.packaging, 1000.0)
        self.assertTrue(pricing.budget_exceeded)
        self.assertLess(pricing.remaining_budget, 0)
        self.assertGreater(pricing.budget_percentage, 100.0)

    def test_sensory_coverage_engine(self):
        coverage = SensoryCoverageEngine.evaluate([self.p1, self.p2])
        self.assertEqual(coverage.sight, 1)
        self.assertEqual(coverage.sound, 1)
        self.assertEqual(coverage.smell, 0)
        self.assertEqual(len(coverage.covered_senses), 2)
        self.assertEqual(coverage.sensory_harmony_score, 40.0)


if __name__ == "__main__":
    unittest.main()
