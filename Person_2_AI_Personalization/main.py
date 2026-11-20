
import os
import json
import logging
from typing import Any

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from groq import Groq

# --------------------------------------------------
# Configuration
# --------------------------------------------------

app = Flask(__name__)

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add deployed frontend origins through FRONTEND_ORIGINS.
# Example:
# FRONTEND_ORIGINS=https://your-frontend.example.com
extra_origins = os.getenv("FRONTEND_ORIGINS", "")
allowed_origins.extend(
    origin.strip()
    for origin in extra_origins.split(",")
    if origin.strip()
)

CORS(
    app,
    resources={
        r"/*": {
            "origins": allowed_origins,
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "OPTIONS"],
        }
    },
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

RECOMMENDATION_API_URL = os.getenv(
    "RECOMMENDATION_API_URL",
    "http://127.0.0.1:5001/api/recommendations",
)

RECOMMENDATION_TOP_N = int(os.getenv("RECOMMENDATION_TOP_N", "5"))

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


# --------------------------------------------------
# Questionnaire mappings
# --------------------------------------------------

EXPERIENCE_LABELS = {
    "cosy_home": "cosy home experiences",
    "outdoors": "outdoor activities and adventures",
    "foodie": "food and culinary experiences",
    "creative": "creative activities and arts",
    "wellness": "wellness and self-care",
    "music": "music",
    "books": "books and reading",
    "social": "social activities and spending time with others",
}

SENSE_LABELS = {
    "scent": "smell",
    "taste": "taste",
    "touch": "touch",
    "sound": "sound",
    "sight": "sight",
}

EMOTION_LABELS = {
    "loved": "love",
    "nostalgic": "nostalgia",
    "calm": "calmness",
    "excited": "happiness",
    "grateful": "thoughtfulness",
    "pampered": "pampering",
    "inspired": "creativity",
    "amused": "amusement",
}

PERSONALITY_LABELS = {
    "calmToAdventurous": ("calm", "adventurous"),
    "practicalToSentimental": ("practical", "sentimental"),
    "classicToQuirky": ("classic", "quirky"),
}


# --------------------------------------------------
# Input validation and normalization
# --------------------------------------------------

def validate_string(value: Any, field: str, required: bool = False) -> str:
    if value is None:
        if required:
            raise ValueError(f"{field} is required.")
        return ""

    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string.")

    return value.strip()


def validate_string_list(value: Any, field: str) -> list[str]:
    if value is None:
        return []

    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list.")

    if not all(isinstance(item, str) for item in value):
        raise ValueError(f"Every item in {field} must be a string.")

    return [item.strip() for item in value if item.strip()]


def validate_personality(personality: Any) -> dict[str, int]:
    if personality is None:
        personality = {}

    if not isinstance(personality, dict):
        raise ValueError("personality must be a JSON object.")

    validated = {}

    for key in PERSONALITY_LABELS:
        value = personality.get(key, 5)

        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"personality.{key} must be an integer from 1 to 10.")

        if value < 1 or value > 10:
            raise ValueError(f"personality.{key} must be between 1 and 10.")

        validated[key] = value

    return validated


def describe_personality(personality: dict[str, int]) -> list[str]:
    descriptors = []

    for key, (low_label, high_label) in PERSONALITY_LABELS.items():
        value = personality[key]

        if value <= 4:
            descriptors.append(low_label)
        elif value >= 7:
            descriptors.append(high_label)
        else:
            descriptors.append("balanced")

    return descriptors


def normalize_questionnaire(data: Any) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")

    recipient = data.get("recipient", {})
    budget = data.get("budget", {})

    if not isinstance(recipient, dict):
        raise ValueError("recipient must be a JSON object.")

    if not isinstance(budget, dict):
        raise ValueError("budget must be a JSON object.")

    recipient_name = validate_string(
        recipient.get("name"),
        "recipient.name",
        required=True,
    )

    relationship = validate_string(
        recipient.get("relationship"),
        "recipient.relationship",
        required=True,
    )

    occasion = validate_string(
        data.get("occasion"),
        "occasion",
        required=True,
    )

    favourite_memory = validate_string(
        data.get("favouriteMemory"),
        "favouriteMemory",
    )

    avoid = validate_string(data.get("avoid"), "avoid")

    experiences = validate_string_list(
        data.get("experiences", []),
        "experiences",
    )

    senses = validate_string_list(
        data.get("senses", []),
        "senses",
    )

    emotions = validate_string_list(
        data.get("emotions", []),
        "emotions",
    )

    personality = validate_personality(data.get("personality"))

    amount = budget.get("amount", 2500)

    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("budget.amount must be a number.")

    if amount <= 0:
        raise ValueError("budget.amount must be greater than zero.")

    currency = budget.get("currency", "INR")

    if currency != "INR":
        raise ValueError("Only INR currency is currently supported.")

    return {
        "recipient_name": recipient_name,
        "relationship": relationship,
        "occasion": occasion,
        "favourite_memory": favourite_memory,
        "experiences": experiences,
        "senses": senses,
        "emotions": emotions,
        "personality": personality,
        "personality_descriptors": describe_personality(personality),
        "budget_inr": amount,
        "avoid": avoid,
    }


# --------------------------------------------------
# Groq profile generation
# --------------------------------------------------

def generate_recipient_profile(questionnaire: dict) -> dict:
    if not groq_client:
        raise RuntimeError("GROQ_API_KEY is not configured on the server.")

    experience_labels = [
        EXPERIENCE_LABELS.get(item, item.replace("_", " "))
        for item in questionnaire["experiences"]
    ]

    sensory_preferences = [
        SENSE_LABELS.get(item, item)
        for item in questionnaire["senses"]
    ]

    emotional_themes = [
        EMOTION_LABELS.get(item, item)
        for item in questionnaire["emotions"]
    ]

    prompt_data = {
        "recipient_name": questionnaire["recipient_name"],
        "relationship": questionnaire["relationship"],
        "occasion": questionnaire["occasion"],
        "favourite_memory": questionnaire["favourite_memory"],
        "interests": experience_labels,
        "sensory_preferences": sensory_preferences,
        "emotional_themes": emotional_themes,
        "personality_descriptors": questionnaire["personality_descriptors"],
        "personality_scale": questionnaire["personality"],
        "budget_inr": questionnaire["budget_inr"],
        "avoid": questionnaire["avoid"],
    }

    system_prompt = """
You are the AI personalization engine for UnboxJoy, a personalized gifting platform.

Analyze the questionnaire and create a concise, useful recipient profile.

Return ONLY valid JSON with these exact keys:
{
  "summary": "A concise recipient profile summary",
  "personalityTraits": ["trait 1", "trait 2"],
  "interests": ["interest 1", "interest 2"],
  "emotionalThemes": ["theme 1", "theme 2"],
  "giftStyle": "A concise description of suitable gift style",
  "recommendationDirections": ["gift direction 1", "gift direction 2"]
}

Rules:
- Use the questionnaire as the source of truth.
- Do not invent personal facts or interests.
- Do not recommend products in this step.
- Keep the summary concise and useful for product matching.
- Respect the recipient's avoid list.
- Keep all values appropriate for a gifting platform.
- Return JSON only.
"""

    completion = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": json.dumps(prompt_data, ensure_ascii=False),
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    content = completion.choices[0].message.content

    if not content:
        raise RuntimeError("The AI model returned an empty response.")

    generated = json.loads(content)

    required_fields = [
        "summary",
        "personalityTraits",
        "interests",
        "emotionalThemes",
        "giftStyle",
        "recommendationDirections",
    ]

    for field in required_fields:
        if field not in generated:
            raise RuntimeError(f"The AI response is missing the field: {field}")

    return generated


# --------------------------------------------------
# Build the profile expected by Person 3
# --------------------------------------------------

def build_person3_profile(questionnaire: dict, generated: dict) -> dict:
    experiences = [
        EXPERIENCE_LABELS.get(item, item.replace("_", " "))
        for item in questionnaire["experiences"]
    ]

    sensory_preferences = [
        SENSE_LABELS.get(item, item)
        for item in questionnaire["senses"]
    ]

    emotional_tags = [
        EMOTION_LABELS.get(item, item)
        for item in questionnaire["emotions"]
    ]

    personality_tags = questionnaire["personality_descriptors"]

    interest_tags = experiences

    matching_tags = {
        "interest_tags": interest_tags,
        "emotion_tags": emotional_tags,
        "sensory_tags": sensory_preferences,
        "personality_tags": personality_tags,
        "style_tags": [generated["giftStyle"]],
        "occasion_tags": [questionnaire["occasion"]],
    }

    return {
        "relationship": questionnaire["relationship"],
        "occasion": questionnaire["occasion"],
        "personality_descriptors": personality_tags,
        "interests": interest_tags,
        "emotional_theme": emotional_tags[0] if emotional_tags else "",
        "sensory_preferences": sensory_preferences,
        "gift_style": generated["giftStyle"],
        "matching_tags": matching_tags,
        "budget_inr": questionnaire["budget_inr"],
        "profile_summary": generated["summary"],
        "recipient_name": questionnaire["recipient_name"],
        "favourite_memory": questionnaire["favourite_memory"],
        "avoid": questionnaire["avoid"],
    }


# --------------------------------------------------
# Forward profile to Person 3 recommendation API
# --------------------------------------------------

def get_recommendations(recipient_profile: dict) -> list[dict]:
    payload = {
        "recipient_profile": recipient_profile,
        "top_n": RECOMMENDATION_TOP_N,
    }

    try:
        response = requests.post(
            RECOMMENDATION_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=(5, 30),
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "The recommendation service timed out. Please try again."
        ) from exc

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "The recommendation service is unavailable. Check that Person 3 is running."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else "unknown"
        raise RuntimeError(
            f"The recommendation service returned HTTP {status_code}."
        ) from exc

    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "The recommendation service returned an invalid JSON response."
        ) from exc

    if isinstance(result, list):
        products = result
    elif isinstance(result, dict):
        products = result.get("recommendations", result.get("products", []))
    else:
        products = []

    if not isinstance(products, list):
        raise RuntimeError("The recommendation service returned an invalid product list.")

    return products


# --------------------------------------------------
# Map Person 3 products to Tanisha's frontend format
# --------------------------------------------------

def map_recommendations(products: list[dict]) -> list[dict]:
    mapped = []

    for product in products:
        if not isinstance(product, dict):
            continue

        raw_price = product.get("price", 0)

        try:
            price = float(raw_price)
            if price.is_integer():
                price = int(price)
        except (TypeError, ValueError):
            price = 0

        reason = (
            product.get("reason")
            or product.get("match_reason")
            or product.get("description")
            or product.get("rationale")
            or "Selected based on the recipient's preferences."
        )

        mapped.append({
            "name": product.get("product_name") or product.get("name") or "Gift item",
            "brand": product.get("brand") or "Not specified",
            "category": product.get("category") or "Gift",
            "price": price,
            "reason": str(reason),
        })

    return mapped


# --------------------------------------------------
# API routes
# --------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "service": "unboxjoy-person2-ai",
        "status": "ok",
        "port": int(os.getenv("PORT", "5000")),
        "recommendation_service_configured": bool(RECOMMENDATION_API_URL),
        "groq_configured": bool(GROQ_API_KEY),
    }), 200


@app.route("/api/personalize", methods=["POST"])
@app.route("/recommendations", methods=["POST"])
def personalize():
    try:
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Request must contain valid JSON."}), 400

        questionnaire = normalize_questionnaire(data)

        generated = generate_recipient_profile(questionnaire)

        recipient_profile = build_person3_profile(
            questionnaire,
            generated,
        )

        # Automatically send the generated profile to Person 3.
        products = get_recommendations(recipient_profile)

        recommendations = map_recommendations(products)

        # Exact response structure requested by Person 1.
        result = {
            "profile": {
                "summary": generated["summary"],
                "personalityTraits": generated["personalityTraits"],
                "interests": generated["interests"],
                "emotionalThemes": generated["emotionalThemes"],
            },
            "recommendations": recommendations,
        }

        return jsonify(result), 200

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    except RuntimeError as exc:
        logger.exception("Personalization or recommendation service error")
        return jsonify({"error": str(exc)}), 502

    except Exception:
        logger.exception("Unexpected error in personalization endpoint")
        return jsonify({
            "error": "An unexpected server error occurred. Please try again."
        }), 500


# --------------------------------------------------
# Run server
# --------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
    )

