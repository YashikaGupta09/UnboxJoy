
# ==========================================
# AI-GUIDED SENSORY GIFT CONCIERGE
# Phase 1: Product Configuration
# ==========================================

# 1. Product categories based on five senses

PRODUCT_CATEGORIES = {
    "sight": [
        "photo_frames",
        "art_prints",
        "decorative_lights",
        "miniature_art",
        "decorative_items"
    ],

    "sound": [
        "music_boxes",
        "mini_speakers",
        "vinyl_records",
        "musical_accessories"
    ],

    "smell": [
        "scented_candles",
        "perfumes",
        "essential_oils",
        "diffusers"
    ],

    "taste": [
        "chocolates",
        "coffee",
        "tea",
        "gourmet_snacks",
        "gift_hampers"
    ],

    "touch": [
        "soft_toys",
        "journals",
        "blankets",
        "handmade_accessories",
        "comfort_items"
    ]
}


# 2. Emotional tags

EMOTIONAL_TAGS = [
    "nostalgia",
    "relaxation",
    "happiness",
    "comfort",
    "adventure",
    "creativity",
    "luxury",
    "self_care",
    "romantic",
    "thoughtfulness"
]


# 3. Interest tags

INTEREST_TAGS = [
    "music",
    "reading",
    "travel",
    "art",
    "food",
    "coffee",
    "nature",
    "photography",
    "gaming",
    "home_decor",
    "fashion",
    "fitness",
    "movies",
    "writing",
    "gardening"
]


# 4. Database requirements

TARGET_PRODUCT_COUNT = 50

TARGET_PRODUCTS_PER_CATEGORY = 10

CURRENCY = "INR"

# We will use these fields for every product.

PRODUCT_FIELDS = [
    "product_id",
    "product_name",
    "brand",
    "category",
    "price",
    "currency",
    "description",
    "emotional_tags",
    "interest_tags",
    "image_url",
    "product_url"
]


# 5. Recommendation algorithm weights
# These will be used in Phase 3.

# RECOMMENDATION_WEIGHTS = {
#     "sensory_match": 0.35,
#     "emotional_match": 0.30,
#     "interest_match": 0.25,
#     "theme_match": 0.10
# }

RECOMMENDATION_WEIGHTS = {
    "sensory": 0.35,
    "emotional": 0.30,
    "interest": 0.25,
    "theme": 0.10
}


if __name__ == "__main__":

    print("PRODUCT DATABASE CONFIGURATION")
    print("--------------------------------")

    print("Categories:", len(PRODUCT_CATEGORIES))
    print("Emotional tags:", len(EMOTIONAL_TAGS))
    print("Interest tags:", len(INTEREST_TAGS))
    print("Target products:", TARGET_PRODUCT_COUNT)

    print("\nProducts per category:")

    for category in PRODUCT_CATEGORIES:
        print(
            category,
            ":", TARGET_PRODUCTS_PER_CATEGORY
        )

    print("\nConfiguration loaded successfully!")
