# Person 4 Integration Contract

## 1. Upstream Input Contract: Person 3 to Person 4

Person 4 consumes recommended products output by Person 3 (or the fallback `inputs/sample_recommendations.json`).

### Expected JSON Payload:
```json
{
  "recipient_profile": {
    "relationship": "best friend",
    "occasion": "birthday",
    "budget_inr": 1500,
    "emotional_theme": "nostalgia",
    "sensory_preferences": ["sight", "touch", "smell"],
    "interests": ["photography", "travel"]
  },
  "recommendations": [
    {
      "product_id": "SIGHT001",
      "product_name": "Sunville Wooden Photo Frame",
      "brand": "Chumbak",
      "category": "sight",
      "price": 399,
      "currency": "INR",
      "description": "Artistic wooden photo frame designed to preserve special memories.",
      "image_url": "https://images.unsplash.com/...",
      "product_url": "https://www.chumbak.com",
      "emotional_tags": ["nostalgia", "thoughtfulness"],
      "interest_tags": ["photography", "home_decor"],
      "match_score": 0.94,
      "match_rationale": "High nostalgia and visual resonance with photography."
    }
  ]
}
```

### Upstream Field Requirements:
- `product_id` (string, unique)
- `product_name` (string)
- `brand` (string)
- `category` (string, one of: `sight`, `sound`, `smell`, `taste`, `touch`)
- `price` (number in INR)
- `image_url` (string, URL)
- `description` (string)

---

## 2. Person 4 API Specifications

### `GET /api/recommendations`
Returns available recommendations grouped by sensory category with recipient profile context.

### `GET /api/packaging`
Returns the 4 packaging options with materials, descriptions, and pricing.

### `POST /api/box/create`
Initializes a mutable box session.
- **Request**:
  ```json
  {
    "session_id": "cust_123",
    "target_budget": 1500,
    "packaging_id": "eco_kraft"
  }
  ```

### `POST /api/box/items`
Adds an item to the box.
- **Request**:
  ```json
  {
    "session_id": "cust_123",
    "product_id": "SIGHT001",
    "strict_budget": true
  }
  ```
- **Response**: Updated box state with item count, pricing, and sensory coverage. Returns HTTP 400 if duplicate, full, or budget exceeded.

### `DELETE /api/box/items/<product_id>`
Removes an item from the box.

### `POST /api/box/auto-assemble`
Executes single-click smart assembly.
- **Request**:
  ```json
  {
    "session_id": "cust_123",
    "target_budget": 1500,
    "packaging_id": "eco_kraft",
    "item_count": 4
  }
  ```

### `POST /api/cart/checkout`
Finalizes box and produces complete order receipt and unboxing sequence.
- **Request**:
  ```json
  {
    "session_id": "cust_123",
    "recipient_name": "Aditi",
    "sender_name": "Karan",
    "occasion": "Birthday Celebration",
    "delivery_address": "Indiranagar, Bangalore",
    "personalized_message": "May this sensory box bring back memories!"
  }
  ```
- **Response**: Complete order receipt with Order ID, itemized financial summary, and unboxing sequence.

---

## 3. Downstream Output: Order Receipt & Unboxing Sequence

```json
{
  "order_id": "UBJ-20261118-A1B2C3",
  "status": "confirmed",
  "created_at": "2026-11-18T22:30:00",
  "estimated_delivery": "Saturday, 21 November 2026",
  "recipient_details": {
    "name": "Aditi",
    "delivery_address": "Indiranagar, Bangalore"
  },
  "packaging": {
    "id": "midnight_luxe",
    "name": "Midnight Matte Luxe Box",
    "fee": 199.0,
    "color_theme": "#1A2A3A"
  },
  "financial_summary": {
    "items_subtotal": 1047.0,
    "packaging_fee": 199.0,
    "tax_gst": 62.3,
    "grand_total": 1308.3,
    "target_budget": 1500.0,
    "remaining_budget": 191.7,
    "budget_exceeded": false
  },
  "unboxing_experience": {
    "reveal_sequence": [ ... ],
    "sensory_balance": "4 of 5 senses awakened",
    "brands_curated": ["Chumbak", "Ekam", "Mason & Co", "Odd Giraffe"]
  }
}
```
