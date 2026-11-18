"""Pricing calculation, tax computation, sensory harmony, and budget validation engine."""

from typing import List, Dict
try:
    from .models import Product, PackagingOption, BoxPricing, SensoryCoverage
except (ImportError, ValueError):
    from models import Product, PackagingOption, BoxPricing, SensoryCoverage

GST_RATE = 0.05  # 5% GST standard on curated gift hampers


class PricingEngine:
    """Calculates all monetary totals, tax, and budget compliance metrics."""

    @staticmethod
    def calculate(
        items: List[Product],
        packaging: PackagingOption,
        target_budget: float,
        discount: float = 0.0
    ) -> BoxPricing:
        """Computes comprehensive pricing and budget utilization."""
        subtotal = round(sum(item.price for item in items), 2)
        packaging_fee = round(packaging.price, 2)
        
        # Calculate GST on subtotal + packaging
        taxable_amount = subtotal + packaging_fee
        tax_gst = round(taxable_amount * GST_RATE, 2)
        
        discount = round(min(discount, taxable_amount), 2)
        grand_total = round(taxable_amount + tax_gst - discount, 2)
        
        target_budget = round(max(0.0, target_budget), 2)
        remaining = round(target_budget - grand_total, 2)
        exceeded = grand_total > target_budget if target_budget > 0 else False
        
        percentage = round((grand_total / target_budget * 100.0), 1) if target_budget > 0 else 0.0

        return BoxPricing(
            items_subtotal=subtotal,
            packaging_fee=packaging_fee,
            tax_gst=tax_gst,
            discount=discount,
            grand_total=grand_total,
            target_budget=target_budget,
            remaining_budget=remaining,
            budget_exceeded=exceeded,
            budget_percentage=percentage,
            currency="INR"
        )


class SensoryCoverageEngine:
    """Evaluates sensory representation across the 5 dimensions."""

    ALL_SENSES = ["sight", "sound", "smell", "taste", "touch"]

    @classmethod
    def evaluate(cls, items: List[Product]) -> SensoryCoverage:
        counts = {sense: 0 for sense in cls.ALL_SENSES}
        for item in items:
            cat = item.category.lower().strip()
            if cat in counts:
                counts[cat] += 1

        covered = [sense for sense, count in counts.items() if count > 0]
        harmony_score = round((len(covered) / float(len(cls.ALL_SENSES))) * 100.0, 1)

        return SensoryCoverage(
            sight=counts["sight"],
            sound=counts["sound"],
            smell=counts["smell"],
            taste=counts["taste"],
            touch=counts["touch"],
            covered_senses=covered,
            sensory_harmony_score=harmony_score
        )
