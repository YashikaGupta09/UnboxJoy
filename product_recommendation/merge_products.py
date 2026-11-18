
import json
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CATEGORY_FILES = [
    "sight_products.json",
    "sound_products.json",
    "smell_products.json",
    "taste_products.json",
    "touch_products.json"
]

EXPECTED_CATEGORIES = {
    "sight", "sound", "smell", "taste", "touch"
}

VALID_EMOTIONAL_TAGS = {
    "nostalgia", "relaxation", "happiness", "comfort",
    "adventure", "creativity", "luxury", "self_care",
    "romantic", "thoughtfulness"
}

VALID_INTEREST_TAGS = {
    "music", "reading", "travel", "art", "food",
    "coffee", "nature", "photography", "gaming",
    "home_decor", "fashion", "fitness", "movies",
    "writing", "gardening"
}

REQUIRED_FIELDS = {
    "product_id", "product_name", "brand", "category",
    "price", "currency", "description",
    "emotional_tags", "interest_tags",
    "image_url", "product_url"
}


def load_products():
    all_products = []

    for filename in CATEGORY_FILES:
        file_path = DATA_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            products = json.load(file)

        if isinstance(products, dict) and "products" in products:
            products = products["products"]

        if not isinstance(products, list):
            raise ValueError(
                f"{filename} must contain a list or an object with a 'products' list."
            )

        all_products.extend(products)

    return all_products


def validate_products(products):
    errors = []

    ids = [p.get("product_id") for p in products]
    duplicate_ids = [
        product_id
        for product_id, count in Counter(ids).items()
        if count > 1
    ]

    if duplicate_ids:
        errors.append(f"Duplicate IDs: {duplicate_ids}")

    category_counts = Counter(
        p.get("category") for p in products
    )

    if set(category_counts) != EXPECTED_CATEGORIES:
        errors.append(
            f"Unexpected category distribution: {dict(category_counts)}"
        )

    for category in EXPECTED_CATEGORIES:
        if category_counts[category] != 10:
            errors.append(
                f"{category}: expected 10 products, "
                f"found {category_counts[category]}"
            )

    for index, product in enumerate(products, start=1):
        missing_fields = REQUIRED_FIELDS - product.keys()

        if missing_fields:
            errors.append(
                f"Product {index}: missing fields {missing_fields}"
            )
            continue

        if not isinstance(product["price"], (int, float)):
            errors.append(
                f"{product['product_id']}: invalid price"
            )
        elif not 200 <= product["price"] <= 1500:
            errors.append(
                f"{product['product_id']}: price outside budget"
            )

        if product["currency"] != "INR":
            errors.append(
                f"{product['product_id']}: currency must be INR"
            )

        invalid_emotions = (
            set(product["emotional_tags"]) - VALID_EMOTIONAL_TAGS
        )

        invalid_interests = (
            set(product["interest_tags"]) - VALID_INTEREST_TAGS
        )

        if invalid_emotions:
            errors.append(
                f"{product['product_id']}: invalid emotional tags "
                f"{invalid_emotions}"
            )

        if invalid_interests:
            errors.append(
                f"{product['product_id']}: invalid interest tags "
                f"{invalid_interests}"
            )

    return errors, category_counts


def main():
    products = load_products()

    errors, category_counts = validate_products(products)

    print("\n========== VALIDATION REPORT ==========")
    print(f"Total products: {len(products)}")

    for category, count in sorted(category_counts.items()):
        print(f"{category}: {count}")

    if errors:
        print("\nVALIDATION FAILED")

        for error in errors:
            print("-", error)

        return

    output_path = DATA_DIR / "products.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4, ensure_ascii=False)

    print("\nVALIDATION PASSED")
    print(f"Master catalogue created: {output_path}")


if __name__ == "__main__":
    main()
