"""End-to-End Integration Tests for Module 4 (Person 4).
Tests the complete flow from Person 3 recommendations to Box Assembly,
Packaging selection, and Cart Order Generation.
"""

import unittest
from Gift_Box_Builder.backend.app import create_app
from Gift_Box_Builder.backend.box_assembler import SmartBoxAssembler
from Gift_Box_Builder.backend.cart import CartManager


class TestEndToEndIntegration(unittest.TestCase):

    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_complete_customer_journey(self):
        """Simulates complete customer journey:
        1. Query recommendations (Person 3 handoff)
        2. Inspect packaging options
        3. Create personalized box
        4. Add products across 4 senses
        5. Verify budget & sensory harmony
        6. Select luxury packaging
        7. Checkout and verify unboxing receipt
        """
        # Step 1: Query recommendations
        rec_res = self.client.get("/api/recommendations")
        self.assertEqual(rec_res.status_code, 200)
        rec_data = rec_res.get_json()
        self.assertGreater(rec_data["total_products"], 0)

        # Step 2: Query packaging options
        pack_res = self.client.get("/api/packaging")
        self.assertEqual(pack_res.status_code, 200)
        pack_options = pack_res.get_json()["packaging_options"]
        self.assertEqual(len(pack_options), 4)

        # Step 3: Initialize box session
        session_id = "e2e_customer_session"
        init_res = self.client.post("/api/box/create", json={
            "session_id": session_id,
            "target_budget": 1500.0,
            "packaging_id": "eco_kraft"
        })
        self.assertEqual(init_res.status_code, 201)

        # Step 4: Add products (Sight, Smell, Taste)
        for pid in ["SIGHT001", "SMELL001", "TASTE001"]:
            add_res = self.client.post("/api/box/items", json={
                "session_id": session_id,
                "product_id": pid
            })
            self.assertEqual(add_res.status_code, 200)

        # Step 5: Check box state and sensory coverage
        state_res = self.client.get(f"/api/box/state?session_id={session_id}")
        self.assertEqual(state_res.status_code, 200)
        box = state_res.get_json()["box"]
        self.assertEqual(box["item_count"], 3)
        self.assertEqual(len(box["sensory_coverage"]["covered_senses"]), 3)
        self.assertFalse(box["pricing"]["budget_exceeded"])

        # Step 6: Select midnight_luxe packaging and add greeting note
        pack_update = self.client.post("/api/box/packaging", json={
            "session_id": session_id,
            "packaging_id": "midnight_luxe",
            "greeting_card": {
                "recipient_name": "Aanya",
                "sender_name": "Priya",
                "message": "Happy 25th Birthday! May this year be filled with unforgettable senses.",
                "font_style": "calligraphy"
            }
        })
        self.assertEqual(pack_update.status_code, 200)
        updated_box = pack_update.get_json()["box"]
        self.assertEqual(updated_box["packaging"]["id"], "midnight_luxe")

        # Step 7: Checkout
        checkout_res = self.client.post("/api/cart/checkout", json={
            "session_id": session_id,
            "recipient_name": "Aanya",
            "sender_name": "Priya",
            "occasion": "25th Birthday",
            "delivery_address": "Flat 402, Sunshine Heights, Mumbai"
        })
        self.assertEqual(checkout_res.status_code, 200)
        order = checkout_res.get_json()["order"]

        # Assert order integrity
        self.assertEqual(order["status"], "confirmed")
        self.assertEqual(order["recipient_details"]["name"], "Aanya")
        self.assertEqual(order["packaging"]["name"], "Midnight Matte Luxe Box")
        self.assertEqual(len(order["items"]), 3)
        self.assertIn("unboxing_experience", order)
        self.assertEqual(len(order["unboxing_experience"]["reveal_sequence"]), 3)
        self.assertGreater(order["financial_summary"]["grand_total"], 0)


if __name__ == "__main__":
    unittest.main()
