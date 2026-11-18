"""Cart and Order Checkout Manager.
Handles order session, summary generation, and unboxing preview data.
"""

from typing import Dict, Any, Optional
import uuid
from datetime import datetime, timedelta

try:
    from .box_assembler import GiftBox
    from .models import GreetingCard
except (ImportError, ValueError):
    from box_assembler import GiftBox
    from models import GreetingCard


class CartManager:
    """Handles checkout validation, order receipt generation, and unboxing preview."""

    @staticmethod
    def generate_order_summary(
        box: GiftBox,
        recipient_name: str = "Valued Recipient",
        sender_name: str = "A Thoughtful Friend",
        occasion: str = "Birthday Celebration",
        delivery_address: str = "Standard Priority Delivery",
        personalized_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generates a complete order summary and unboxing preview."""
        if not box.items:
            raise ValueError("Cannot checkout an empty gift box.")

        pricing = box.get_pricing()
        coverage = box.get_sensory_coverage()

        # Update greeting card if message provided
        if personalized_message:
            box.set_greeting_card(
                recipient_name=recipient_name,
                sender_name=sender_name,
                message=personalized_message
            )

        now = datetime.now()
        order_id = f"UBJ-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        estimated_delivery = (now + timedelta(days=3)).strftime("%A, %d %B %Y")

        unboxing_reveal_sequence = []
        for idx, item in enumerate(box.items, start=1):
            unboxing_reveal_sequence.append({
                "reveal_step": idx,
                "product_id": item.product_id,
                "product_name": item.product_name,
                "brand": item.brand,
                "category": item.category,
                "price": item.price,
                "sensory_highlight": f"Engages your sense of {item.category.upper()}",
                "image_url": item.image_url
            })

        order_receipt = {
            "order_id": order_id,
            "status": "confirmed",
            "created_at": now.isoformat(),
            "estimated_delivery": estimated_delivery,
            "occasion": occasion,
            "recipient_details": {
                "name": recipient_name,
                "delivery_address": delivery_address
            },
            "sender_details": {
                "name": sender_name
            },
            "packaging": {
                "id": box.packaging.id,
                "name": box.packaging.name,
                "material": box.packaging.material,
                "fee": box.packaging.price,
                "color_theme": box.packaging.color_theme,
                "ribbon_color": box.packaging.ribbon_color,
                "unboxing_note": "Hand-tied with double-faced ribbon and cushioned with eco-friendly paper shreds."
            },
            "greeting_card": box.card.to_dict() if box.card else {
                "recipient_name": recipient_name,
                "sender_name": sender_name,
                "message": f"Wishing you a memorable {occasion}!",
                "font_style": "calligraphy"
            },
            "item_count": len(box.items),
            "items": [item.to_dict() for item in box.items],
            "financial_summary": pricing.to_dict(),
            "sensory_coverage": coverage.to_dict(),
            "unboxing_experience": {
                "box_headline": f"A Personalized Sensory Journey for {recipient_name}",
                "reveal_sequence": unboxing_reveal_sequence,
                "sensory_balance": f"{len(coverage.covered_senses)} of 5 senses awakened",
                "brands_curated": list(set(item.brand for item in box.items))
            }
        }

        return order_receipt
