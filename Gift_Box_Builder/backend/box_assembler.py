"""Gift Box state manager and Smart Auto-Assembly Optimizer.
Assembles 3 to 5 multi-brand sensory items within budget constraints.
"""

from typing import List, Dict, Optional, Tuple, Any
import copy

try:
    from .models import Product, PackagingOption, GreetingCard, BoxPricing, SensoryCoverage
    from .packaging import get_packaging_by_id, DEFAULT_PACKAGING_ID
    from .pricing import PricingEngine, SensoryCoverageEngine
except (ImportError, ValueError):
    from models import Product, PackagingOption, GreetingCard, BoxPricing, SensoryCoverage
    from packaging import get_packaging_by_id, DEFAULT_PACKAGING_ID
    from pricing import PricingEngine, SensoryCoverageEngine


class GiftBox:
    """Represents a mutable customer gift box session."""

    def __init__(
        self,
        session_id: str = "default_session",
        target_budget: float = 1500.0,
        packaging_id: str = DEFAULT_PACKAGING_ID,
        max_items: int = 5,
        min_items: int = 3
    ):
        self.session_id = session_id
        self.target_budget = float(target_budget)
        self.packaging: PackagingOption = get_packaging_by_id(packaging_id)
        self.card: Optional[GreetingCard] = None
        self.max_items = max_items
        self.min_items = min_items
        self.items: List[Product] = []

    def add_item(self, product: Product, strict_budget: bool = True) -> Tuple[bool, str]:
        """Adds a product to the box, validating duplicate, capacity, and budget."""
        # 1. Check duplicate
        if any(item.product_id == product.product_id for item in self.items):
            return False, f"Product '{product.product_name}' is already in the box."

        # 2. Check capacity
        if len(self.items) >= self.max_items:
            return False, f"The gift box is full (maximum {self.max_items} items allowed)."

        # 3. Check budget constraint
        temp_items = self.items + [product]
        pricing = PricingEngine.calculate(temp_items, self.packaging, self.target_budget)
        if strict_budget and pricing.budget_exceeded:
            deficit = abs(pricing.remaining_budget)
            return False, f"Adding this item exceeds your ₹{self.target_budget:.0f} budget by ₹{deficit:.2f}."

        self.items.append(product)
        return True, f"Added '{product.product_name}' to your gift box."

    def remove_item(self, product_id: str) -> Tuple[bool, str]:
        """Removes a product by product_id."""
        initial_count = len(self.items)
        self.items = [item for item in self.items if item.product_id != product_id]
        if len(self.items) < initial_count:
            return True, "Item removed from your gift box."
        return False, "Item not found in your gift box."

    def set_packaging(self, packaging_id: str) -> Tuple[bool, str]:
        """Updates the packaging style."""
        self.packaging = get_packaging_by_id(packaging_id)
        return True, f"Selected packaging: {self.packaging.name}"

    def set_greeting_card(
        self,
        recipient_name: str,
        sender_name: str,
        message: str,
        font_style: str = "calligraphy",
        card_theme: str = "botanical"
    ) -> None:
        """Attaches a personalized greeting card to the box."""
        self.card = GreetingCard(
            recipient_name=recipient_name,
            sender_name=sender_name,
            message=message,
            font_style=font_style,
            card_theme=card_theme
        )

    def clear(self) -> None:
        """Empties all items from the box."""
        self.items.clear()

    def get_pricing(self) -> BoxPricing:
        """Returns computed pricing breakdown."""
        return PricingEngine.calculate(self.items, self.packaging, self.target_budget)

    def get_sensory_coverage(self) -> SensoryCoverage:
        """Returns sensory coverage across the 5 senses."""
        return SensoryCoverageEngine.evaluate(self.items)

    def to_dict(self) -> Dict[str, Any]:
        """Returns comprehensive box state for API or UI consumption."""
        pricing = self.get_pricing()
        coverage = self.get_sensory_coverage()
        unique_brands = list(set(item.brand for item in self.items))

        return {
            "session_id": self.session_id,
            "target_budget": self.target_budget,
            "item_count": len(self.items),
            "max_items": self.max_items,
            "min_items": self.min_items,
            "is_complete": len(self.items) >= self.min_items,
            "items": [item.to_dict() for item in self.items],
            "packaging": self.packaging.to_dict(),
            "card": self.card.to_dict() if self.card else None,
            "pricing": pricing.to_dict(),
            "sensory_coverage": coverage.to_dict(),
            "brands_included": unique_brands,
            "brand_diversity_score": round(len(unique_brands) / max(1, len(self.items)) * 100.0, 1)
        }


class SmartBoxAssembler:
    """Automatically assembles an optimal gift box from recommended products."""

    @classmethod
    def auto_assemble(
        cls,
        candidate_products: List[Product],
        target_budget: float,
        packaging_id: str = DEFAULT_PACKAGING_ID,
        target_item_count: int = 4
    ) -> Tuple[Optional[GiftBox], str]:
        """Selects 3 to 5 multi-brand, sensory-diverse items within the budget.
        
        Algorithm:
        1. Group candidates by category (sight, sound, smell, taste, touch).
        2. Sort candidates within each category by match_score descending, then price ascending.
        3. Iterate across distinct categories to build a multi-sensory, multi-brand combination.
        4. Validate that total cost (subtotal + packaging + tax) stays within budget.
        """
        if not candidate_products:
            return None, "No candidate products available for auto-assembly."

        box = GiftBox(
            session_id="auto_assembled",
            target_budget=target_budget,
            packaging_id=packaging_id
        )

        # Categorize candidates
        by_category: Dict[str, List[Product]] = {
            "sight": [], "sound": [], "smell": [], "taste": [], "touch": []
        }
        for p in candidate_products:
            cat = p.category.lower().strip()
            if cat in by_category:
                by_category[cat].append(p)

        # Sort within category: primary by match_score desc (if available), secondary by price asc
        for cat in by_category:
            by_category[cat].sort(
                key=lambda x: (x.match_score if x.match_score is not None else 0.5, -x.price),
                reverse=True
            )

        # Desired sensory order for balanced unboxing experience
        sensory_priority = ["smell", "taste", "sight", "touch", "sound"]

        # Greedy selection with brand diversity
        selected_brands = set()
        for cat in sensory_priority:
            if len(box.items) >= target_item_count:
                break

            for prod in by_category.get(cat, []):
                if prod.brand in selected_brands:
                    continue  # Ensure brand diversity

                # Test if adding this product keeps within budget
                test_items = box.items + [prod]
                pricing = PricingEngine.calculate(test_items, box.packaging, target_budget)
                if not pricing.budget_exceeded:
                    box.items.append(prod)
                    selected_brands.add(prod.brand)
                    break

        # If we couldn't get at least 3 items with distinct senses, try any category within budget
        if len(box.items) < box.min_items:
            for p in sorted(candidate_products, key=lambda x: x.price):
                if any(item.product_id == p.product_id for item in box.items):
                    continue
                if p.brand in selected_brands and len(box.items) >= 2:
                    continue
                test_items = box.items + [p]
                pricing = PricingEngine.calculate(test_items, box.packaging, target_budget)
                if not pricing.budget_exceeded:
                    box.items.append(p)
                    selected_brands.add(p.brand)
                if len(box.items) >= target_item_count:
                    break

        if len(box.items) < box.min_items:
            return box, (
                f"Auto-assembled partial box with {len(box.items)} item(s). "
                f"Consider increasing budget to reach recommended {box.min_items} items."
            )

        pricing = box.get_pricing()
        return box, (
            f"Successfully auto-assembled sensory gift box with {len(box.items)} items "
            f"across {len(box.get_sensory_coverage().covered_senses)} senses for ₹{pricing.grand_total:.2f}."
        )
