
# UnboxJoy – Product Recommendation API

## Base URL

http://127.0.0.1:5001

## 1. Health Check

- Method: GET
- Endpoint: /api/health
- Purpose: Checks whether the recommendation service is running.
- Request Body: None

### Successful Response (200)

{
    "status": "success",
    "message": "Recommendation service is running."
}

---

## 2. Get All Products

- Method: GET
- Endpoint: /api/products
- Purpose: Retrieves all products from the product database.
- Request Body: None

### Successful Response (200)

{
    "total_products": 50,
    "products": [
        {
            "product_id": "SIGHT001",
            "product_name": "Chumbak Sunville Photo Frame",
            "brand": "Chumbak",
            "category": "sight",
            "price": 899,
            "currency": "INR",
            "description": "...",
            "emotional_tags": ["nostalgia", "happiness"],
            "interest_tags": ["photography", "home_decor"],
            "theme_tags": ["nostalgia", "personalized_memories"],
            "image_url": "",
            "product_url": "https://www.chumbak.com"
        }
    ]
}

Note: The products array contains all 50 products.

---

## 3. Generate Personalized Recommendations

- Method: POST
- Endpoint: /api/recommendations
- Purpose: Generates personalized product recommendations using the recipient profile received from Person 2.

### Request Body

{
    "recipient_profile": {
        "relationship": "best friend",
        "occasion": "birthday",
        "budget_inr": 1500,
        "emotional_theme": "nostalgia",
        "sensory_preferences": ["sight", "touch"],
        "interests": ["photography", "travel"],
        "matching_tags": {
            "interest_tags": ["photography", "travel"],
            "emotion_tags": ["nostalgia"],
            "sensory_tags": ["sight", "touch"]
        }
    },
    "top_n": 5
}

### Successful Response (200)

{
    "recipient_profile": {
        "relationship": "best friend",
        "occasion": "birthday",
        "budget_inr": 1500,
        "emotional_theme": "nostalgia",
        "sensory_preferences": ["sight", "touch"],
        "interests": ["photography", "travel"]
    },
    "recommendations": [
        {
            "product_id": "SIGHT001",
            "product_name": "Chumbak Sunville Photo Frame",
            "brand": "Chumbak",
            "category": "sight",
            "price": 899,
            "currency": "INR",
            "description": "...",
            "image_url": "",
            "product_url": "https://www.chumbak.com",
            "emotional_tags": ["nostalgia", "happiness"],
            "interest_tags": ["photography", "home_decor"],
            "match_score": 0.875
        }
    ]
}

Note: The recommendations array contains up to top_n products.

### Error Responses

HTTP 400 – Bad Request

Returned when:
- recipient_profile is missing or invalid.
- budget_inr is missing or invalid.
- top_n is not a positive integer.

---

## Recommendation Scoring

The recommendation engine uses the following weights:

- Sensory match: 35%
- Emotional match: 30%
- Interest match: 25%
- Theme match: 10%

Products are filtered according to the recipient's budget and ranked using their final match scores. The engine also prioritizes category diversity.

## Product Categories

- sight
- sound
- smell
- taste
- touch

## Important Integration Notes

1. Person 2 must provide the recipient profile in the agreed JSON structure.
2. The recipient profile must include budget_inr and matching_tags.
3. Person 4 can use the recommendations returned by the POST API to build the gift box.
4. Image URLs may currently be empty. The frontend should support placeholder images.
5. All prices are in INR.
