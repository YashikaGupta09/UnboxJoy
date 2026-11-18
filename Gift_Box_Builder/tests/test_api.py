"""Integration tests for Person 4 Flask REST API endpoints."""

import unittest
import json
from Gift_Box_Builder.backend.app import create_app


class TestGiftBoxAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("products_loaded", data)

    def test_get_recommendations(self):
        res = self.client.get("/api/recommendations")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("recipient_profile", data)
        self.assertIn("by_sensory_category", data)
        self.assertIn("sight", data["by_sensory_category"])
        self.assertIn("touch", data["by_sensory_category"])

    def test_get_packaging_options(self):
        res = self.client.get("/api/packaging")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("packaging_options", data)
        self.assertEqual(len(data["packaging_options"]), 4)

    def test_box_crud_flow(self):
        # 1. Initialize box
        res = self.client.post("/api/box/create", json={
            "session_id": "test_session_1",
            "target_budget": 2000.0,
            "packaging_id": "eco_kraft"
        })
        self.assertEqual(res.status_code, 201)

        # 2. Add item
        add_res = self.client.post("/api/box/items", json={
            "session_id": "test_session_1",
            "product_id": "SIGHT001"
        })
        self.assertEqual(add_res.status_code, 200)
        box_data = add_res.get_json()["box"]
        self.assertEqual(box_data["item_count"], 1)

        # 3. Get state
        state_res = self.client.get("/api/box/state?session_id=test_session_1")
        self.assertEqual(state_res.status_code, 200)
        self.assertEqual(state_res.get_json()["box"]["item_count"], 1)

        # 4. Remove item
        del_res = self.client.delete("/api/box/items/SIGHT001?session_id=test_session_1")
        self.assertEqual(del_res.status_code, 200)
        self.assertEqual(del_res.get_json()["box"]["item_count"], 0)

    def test_auto_assemble_endpoint(self):
        res = self.client.post("/api/box/auto-assemble", json={
            "session_id": "auto_test_session",
            "target_budget": 1500.0,
            "packaging_id": "eco_kraft",
            "item_count": 4
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        box = data["box"]
        self.assertGreaterEqual(box["item_count"], 3)
        self.assertFalse(box["pricing"]["budget_exceeded"])

    def test_checkout_endpoint(self):
        # Assemble box first
        self.client.post("/api/box/auto-assemble", json={
            "session_id": "checkout_session",
            "target_budget": 1500.0
        })

        # Checkout
        checkout_res = self.client.post("/api/cart/checkout", json={
            "session_id": "checkout_session",
            "recipient_name": "Rohan",
            "sender_name": "Vanshika",
            "occasion": "Birthday",
            "personalized_message": "Happy Birthday Rohan! Hope you love this sensory box."
        })
        self.assertEqual(checkout_res.status_code, 200)
        order = checkout_res.get_json()["order"]
        self.assertEqual(order["status"], "confirmed")
        self.assertEqual(order["recipient_details"]["name"], "Rohan")
        self.assertIn("unboxing_experience", order)


if __name__ == "__main__":
    unittest.main()
