"""Automated Test Runner and Evaluation Artifact Generator for Person 4.
Executes all unit and integration tests and writes structured TC01-TC05
evaluation logs to test_results/.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import unittest
import json
from datetime import datetime

from Gift_Box_Builder.backend.app import create_app
from Gift_Box_Builder.backend.models import Product
from Gift_Box_Builder.backend.box_assembler import GiftBox, SmartBoxAssembler
from Gift_Box_Builder.backend.cart import CartManager
from Gift_Box_Builder.backend.pricing import PricingEngine, SensoryCoverageEngine
from Gift_Box_Builder.backend.packaging import get_all_packaging_options, get_packaging_by_id

RESULTS_DIR = Path(__file__).resolve().parent / "test_results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_evaluation_artifacts():
    timestamp = datetime.now().isoformat()
    print("==================================================")
    print("  PERSON 4: GIFT BOX BUILDER EVALUATION RUNNER")
    print("==================================================")

    # ---------------- TC01: Box Customization ----------------
    print("\nRunning TC01: Box Customization & Slot Management...")
    box = GiftBox(target_budget=2000.0)
    p1 = Product("SIGHT001", "Photo Frame", "Chumbak", "sight", 399.0)
    p2 = Product("SMELL001", "Lavender Candle", "Ekam", "smell", 349.0)
    
    add1, msg1 = box.add_item(p1)
    add2, msg2 = box.add_item(p2)
    add_dup, msg_dup = box.add_item(p1)
    rem, msg_rem = box.remove_item(p1.product_id)

    tc01_result = {
        "test_case_id": "TC01",
        "name": "Box Customization & Item Slot Management",
        "timestamp": timestamp,
        "status": "PASSED" if (add1 and add2 and not add_dup and rem) else "FAILED",
        "assertions": {
            "item_addition": add1,
            "duplicate_prevention": not add_dup,
            "item_removal": rem,
            "active_item_count": len(box.items)
        },
        "details": "Verified item addition, duplicate rejection, and item removal."
    }
    with open(RESULTS_DIR / "TC01_box_customization.json", "w") as f:
        json.dump(tc01_result, f, indent=2)

    # ---------------- TC02: Smart Auto-Assembly ----------------
    print("Running TC02: Smart Auto-Assembly Knapsack Optimization...")
    candidates = [
        Product("SIGHT001", "Photo Frame", "Chumbak", "sight", 399.0, match_score=0.94),
        Product("SOUND001", "Speaker", "boAt", "sound", 499.0, match_score=0.82),
        Product("SMELL001", "Candle", "Ekam", "smell", 349.0, match_score=0.93),
        Product("TASTE001", "Chocolate", "Mason & Co", "taste", 299.0, match_score=0.89),
        Product("TOUCH001", "Journal", "Odd Giraffe", "touch", 299.0, match_score=0.92)
    ]
    assembled_box, asm_msg = SmartBoxAssembler.auto_assemble(
        candidates, target_budget=1500.0, packaging_id="eco_kraft", target_item_count=4
    )
    pricing = assembled_box.get_pricing()
    coverage = assembled_box.get_sensory_coverage()

    tc02_result = {
        "test_case_id": "TC02",
        "name": "Smart Auto-Assembly Knapsack Optimization",
        "timestamp": timestamp,
        "status": "PASSED" if (not pricing.budget_exceeded and len(assembled_box.items) >= 3) else "FAILED",
        "items_selected": [item.product_name for item in assembled_box.items],
        "senses_covered": coverage.covered_senses,
        "sensory_harmony_score": coverage.sensory_harmony_score,
        "grand_total": pricing.grand_total,
        "target_budget": pricing.target_budget,
        "budget_exceeded": pricing.budget_exceeded,
        "details": asm_msg
    }
    with open(RESULTS_DIR / "TC02_smart_auto_assembly.json", "w") as f:
        json.dump(tc02_result, f, indent=2)

    # ---------------- TC03: Budget Boundary & Pricing ----------------
    print("Running TC03: Budget Boundary & Pricing Engine Validation...")
    strict_box = GiftBox(target_budget=500.0, packaging_id="eco_kraft")
    expensive_prod = Product("EXP001", "Luxury Watch", "Titan", "sight", 800.0)
    add_exp, exp_msg = strict_box.add_item(expensive_prod, strict_budget=True)
    
    tc03_result = {
        "test_case_id": "TC03",
        "name": "Budget Boundary & Pricing Engine Validation",
        "timestamp": timestamp,
        "status": "PASSED" if not add_exp else "FAILED",
        "rejection_message": exp_msg,
        "budget_limit": 500.0,
        "attempted_item_price": expensive_prod.price,
        "details": "Verified strict budget validation prevents over-budget items."
    }
    with open(RESULTS_DIR / "TC03_budget_boundary_validation.json", "w") as f:
        json.dump(tc03_result, f, indent=2)

    # ---------------- TC04: Brand Diversity ----------------
    print("Running TC04: Multi-Brand Diversity Guarantee...")
    brands_in_box = [item.brand for item in assembled_box.items]
    is_diverse = len(brands_in_box) == len(set(brands_in_box))

    tc04_result = {
        "test_case_id": "TC04",
        "name": "Multi-Brand Diversity Guarantee",
        "timestamp": timestamp,
        "status": "PASSED" if is_diverse else "FAILED",
        "brands_in_box": brands_in_box,
        "unique_brands_count": len(set(brands_in_box)),
        "total_items": len(brands_in_box),
        "diversity_ratio": len(set(brands_in_box)) / max(1, len(brands_in_box)),
        "details": "Guaranteed zero brand monopoly in auto-assembled box."
    }
    with open(RESULTS_DIR / "TC04_brand_diversity_evaluation.json", "w") as f:
        json.dump(tc04_result, f, indent=2)

    # ---------------- TC05: End-to-End Checkout & Unboxing ----------------
    print("Running TC05: End-to-End Checkout & Unboxing Experience...")
    assembled_box.set_packaging("midnight_luxe")
    order = CartManager.generate_order_summary(
        box=assembled_box,
        recipient_name="Aditi Sharma",
        sender_name="Karan Verma",
        occasion="Birthday Celebration",
        delivery_address="Indiranagar, Bangalore",
        personalized_message="To laughter and sweet memories! Happy Birthday!"
    )
    tc05_result = {
        "test_case_id": "TC05",
        "name": "End-to-End Checkout & Unboxing Experience",
        "timestamp": timestamp,
        "status": "PASSED" if order.get("order_id") else "FAILED",
        "order_id": order["order_id"],
        "status_code": order["status"],
        "recipient": order["recipient_details"]["name"],
        "packaging": order["packaging"]["name"],
        "unboxing_reveal_steps": len(order["unboxing_experience"]["reveal_sequence"]),
        "grand_total": order["financial_summary"]["grand_total"],
        "details": "Verified full order summary and unboxing reveal sequence generation."
    }
    with open(RESULTS_DIR / "TC05_e2e_checkout_unboxing.json", "w") as f:
        json.dump(tc05_result, f, indent=2)

    print("\nAll 5 evaluation artifacts written to Gift_Box_Builder/test_results/")


if __name__ == "__main__":
    generate_evaluation_artifacts()
    # Run unittests
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent / "tests"))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        exit(1)
