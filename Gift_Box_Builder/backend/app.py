"""Flask REST API backend -  Gift Box Builder, Cart & Backend.
Serves product recommendations, gift box manipulation, packaging selection, and checkout.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys
from pathlib import Path
import json
import os
from typing import Dict, List, Optional

# Ensure package directory and project root are in sys.path for direct execution
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from .models import Product
    from .packaging import get_all_packaging_options, get_packaging_by_id, DEFAULT_PACKAGING_ID
    from .box_assembler import GiftBox, SmartBoxAssembler
    from .cart import CartManager
except (ImportError, ValueError):
    from models import Product
    from packaging import get_all_packaging_options, get_packaging_by_id, DEFAULT_PACKAGING_ID
    from box_assembler import GiftBox, SmartBoxAssembler
    from cart import CartManager

BASE_DIR = BACKEND_DIR.parent
FRONTEND_DIR = BASE_DIR / "frontend"
INPUTS_DIR = BASE_DIR / "inputs"
MODULE3_OUTPUT_PATH = BASE_DIR.parent / "UnboxJoy" / "product_recommendation" / "recommendations_output.json"
MODULE3_DATA_PATH = BASE_DIR.parent / "UnboxJoy" / "product_recommendation" / "data" / "products.json"


def create_app(test_config: Optional[dict] = None) -> Flask:
    app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
    CORS(app)

    if test_config:
        app.config.update(test_config)

    # In-memory session store (keyed by session_id)
    sessions: Dict[str, GiftBox] = {}

    def get_or_create_session(session_id: str = "default_session", budget: float = 1500.0) -> GiftBox:
        if session_id not in sessions:
            sessions[session_id] = GiftBox(session_id=session_id, target_budget=budget)
        return sessions[session_id]

    def load_catalog_products() -> List[Product]:
        """Loads products from inputs/sample_recommendations.json, Module 3 output, or products.json."""
        # 1. Primary: Load module contract catalog
        sample_path = INPUTS_DIR / "sample_recommendations.json"
        if sample_path.exists():
            try:
                with open(sample_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    items = data.get("recommendations", [])
                    if items:
                        return [Product.from_dict(item) for item in items]
            except Exception as e:
                app.logger.warning(f"Could not load sample_recommendations: {e}")

        # 2. Try Person 3's generated output
        if MODULE3_OUTPUT_PATH.exists():
            try:
                with open(MODULE3_OUTPUT_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    items = data.get("recommendations", [])
                    if items:
                        return [Product.from_dict(item) for item in items]
            except Exception as e:
                app.logger.warning(f"Could not load from recommendations_output.json: {e}")

        # 3. Try Person 3's master products.json
        if MODULE3_DATA_PATH.exists():
            try:
                with open(MODULE3_DATA_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    items = data.get("products", data) if isinstance(data, dict) else data
                    if items:
                        return [Product.from_dict(item) for item in items]
            except Exception as e:
                app.logger.warning(f"Could not load Module 3 products: {e}")

        return []

    # Cache products
    catalog_products = load_catalog_products()

    # ---------------- API ROUTES ----------------

    @app.route("/", methods=["GET"])
    def serve_frontend():
        index_file = FRONTEND_DIR / "index.html"
        if index_file.exists():
            return send_from_directory(str(FRONTEND_DIR), "index.html")
        return jsonify({
            "message": "UnboxJoy Gift Box Builder API is active.",
            "frontend": "Place index.html in Gift_Box_Builder/frontend/"
        })

    @app.route("/<path:path>", methods=["GET"])
    def serve_static(path):
        target_file = FRONTEND_DIR / path
        if target_file.exists():
            return send_from_directory(str(FRONTEND_DIR), path)
        return jsonify({"error": "File not found"}), 404

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy",
            "module": "Module 4: Gift Box Builder, Cart & Backend",
            "version": "1.0.0",
            "products_loaded": len(catalog_products)
        })

    @app.route("/api/recommendations", methods=["GET"])
    def get_recommendations():
        """Returns recommended products with sensory categorization and recipient profile."""
        profile = {
            "relationship": "best friend",
            "occasion": "Birthday",
            "budget_inr": 1500,
            "emotional_theme": "nostalgia",
            "sensory_preferences": ["sight", "touch", "smell"]
        }

        # Check Person 3 generated output first
        if MODULE3_OUTPUT_PATH.exists():
            try:
                with open(MODULE3_OUTPUT_PATH, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    if "recipient_profile" in d:
                        profile = d["recipient_profile"]
            except Exception:
                pass
        elif (INPUTS_DIR / "sample_recommendations.json").exists():
            try:
                with open(INPUTS_DIR / "sample_recommendations.json", "r", encoding="utf-8") as f:
                    d = json.load(f)
                    if "recipient_profile" in d:
                        profile = d["recipient_profile"]
            except Exception:
                pass

        by_sense = {"sight": [], "sound": [], "smell": [], "taste": [], "touch": []}
        for p in catalog_products:
            cat = p.category.lower().strip()
            if cat in by_sense:
                by_sense[cat].append(p.to_dict())

        return jsonify({
            "recipient_profile": profile,
            "total_products": len(catalog_products),
            "by_sensory_category": by_sense,
            "all_recommendations": [p.to_dict() for p in catalog_products]
        })

    @app.route("/api/packaging", methods=["GET"])
    def get_packaging():
        """Returns all 4 packaging options with materials and pricing."""
        options = [opt.to_dict() for opt in get_all_packaging_options()]
        return jsonify({"packaging_options": options, "default_id": DEFAULT_PACKAGING_ID})

    @app.route("/api/box/create", methods=["POST"])
    def create_box():
        """Initializes or resets a gift box session."""
        data = request.get_json() or {}
        session_id = data.get("session_id", "default_session")
        budget = float(data.get("target_budget", 1500.0))
        packaging_id = data.get("packaging_id", DEFAULT_PACKAGING_ID)

        box = GiftBox(
            session_id=session_id,
            target_budget=budget,
            packaging_id=packaging_id
        )
        sessions[session_id] = box

        return jsonify({
            "message": f"Gift box session '{session_id}' initialized with ₹{budget:.0f} budget.",
            "box": box.to_dict()
        }), 201

    @app.route("/api/box/state", methods=["GET"])
    def get_box_state():
        """Returns full state, sensory coverage, and pricing of the active box."""
        session_id = request.args.get("session_id", "default_session")
        box = get_or_create_session(session_id)
        return jsonify({"box": box.to_dict()})

    @app.route("/api/box/items", methods=["POST"])
    def add_box_item():
        """Adds a recommended product to the box, validating duplicate and budget."""
        data = request.get_json() or {}
        session_id = data.get("session_id", "default_session")
        product_id = data.get("product_id")
        strict_budget = data.get("strict_budget", True)

        if not product_id:
            return jsonify({"error": "Missing 'product_id'"}), 400

        box = get_or_create_session(session_id)
        prod = next((p for p in catalog_products if p.product_id == product_id), None)
        if not prod:
            return jsonify({"error": f"Product with ID '{product_id}' not found in catalog."}), 404

        success, msg = box.add_item(prod, strict_budget=strict_budget)
        status_code = 200 if success else 400

        return jsonify({
            "success": success,
            "message": msg,
            "box": box.to_dict()
        }), status_code

    @app.route("/api/box/items/<product_id>", methods=["DELETE"])
    def remove_box_item(product_id):
        """Removes a product from the box."""
        session_id = request.args.get("session_id", "default_session")
        box = get_or_create_session(session_id)

        success, msg = box.remove_item(product_id)
        status_code = 200 if success else 404

        return jsonify({
            "success": success,
            "message": msg,
            "box": box.to_dict()
        }), status_code

    @app.route("/api/box/auto-assemble", methods=["POST"])
    def auto_assemble():
        """Runs the smart knapsack optimizer to assemble a multi-sensory, multi-brand box."""
        data = request.get_json() or {}
        session_id = data.get("session_id", "default_session")
        box = get_or_create_session(session_id)

        target_budget = float(data.get("target_budget", box.target_budget))
        packaging_id = data.get("packaging_id", box.packaging.id)
        item_count = int(data.get("item_count", 4))

        assembled_box, msg = SmartBoxAssembler.auto_assemble(
            candidate_products=catalog_products,
            target_budget=target_budget,
            packaging_id=packaging_id,
            target_item_count=item_count
        )

        if assembled_box:
            assembled_box.session_id = session_id
            sessions[session_id] = assembled_box
            return jsonify({
                "success": True,
                "message": msg,
                "box": assembled_box.to_dict()
            })
        else:
            return jsonify({
                "success": False,
                "message": msg,
                "box": box.to_dict()
            }), 400

    @app.route("/api/box/packaging", methods=["POST"])
    def update_packaging():
        """Updates packaging option and greeting card note."""
        data = request.get_json() or {}
        session_id = data.get("session_id", "default_session")
        box = get_or_create_session(session_id)

        packaging_id = data.get("packaging_id")
        if packaging_id:
            box.set_packaging(packaging_id)

        card_data = data.get("greeting_card")
        if card_data:
            box.set_greeting_card(
                recipient_name=card_data.get("recipient_name", ""),
                sender_name=card_data.get("sender_name", ""),
                message=card_data.get("message", ""),
                font_style=card_data.get("font_style", "calligraphy"),
                card_theme=card_data.get("card_theme", "botanical")
            )

        return jsonify({
            "message": "Packaging preferences updated.",
            "box": box.to_dict()
        })

    @app.route("/api/cart/checkout", methods=["POST"])
    def checkout():
        """Finalizes order, generates receipt, and produces unboxing preview data."""
        data = request.get_json() or {}
        session_id = data.get("session_id", "default_session")
        box = get_or_create_session(session_id)

        if not box.items:
            return jsonify({
                "error": "Cannot checkout an empty gift box. Please add at least 3 items."
            }), 400

        recipient_name = data.get("recipient_name", "Best Friend")
        sender_name = data.get("sender_name", "A Thoughtful Friend")
        occasion = data.get("occasion", "Birthday Celebration")
        delivery_address = data.get("delivery_address", "Express Home Delivery")
        message = data.get("personalized_message")

        try:
            order_summary = CartManager.generate_order_summary(
                box=box,
                recipient_name=recipient_name,
                sender_name=sender_name,
                occasion=occasion,
                delivery_address=delivery_address,
                personalized_message=message
            )
            return jsonify({
                "success": True,
                "message": "Order successfully placed!",
                "order": order_summary
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5002))
    print(f"Starting UnboxJoy Gift Box Builder API on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
