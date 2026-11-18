
import json
from pathlib import Path


# Locate products.json relative to the project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = PROJECT_ROOT / "data" / "products.json"


# Fields that every product must contain
REQUIRED_FIELDS = [
    "product_id",
    "product_name",
    "brand",
    "category",
    "price",
    "currency",
    "description",
    "emotional_tags",
    "interest_tags",
    "theme_tags",
    "image_url",
    "product_url"
]


def validate_products(products):
    """Validate the structure and basic data of every product."""

    if not isinstance(products, list):
        raise ValueError("'products' must contain a list.")

    if not products:
        raise ValueError("The product database is empty.")

    valid_categories = {"sight", "sound", "smell", "taste", "touch"}
    seen_ids = set()

    for index, product in enumerate(products):

        if not isinstance(product, dict):
            raise ValueError(f"Product at index {index} must be an object.")

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in product:
                raise ValueError(
                    f"Product at index {index} is missing '{field}'."
                )

        # Check unique product IDs
        product_id = product["product_id"]

        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError(f"Invalid product ID at index {index}.")

        if product_id in seen_ids:
            raise ValueError(f"Duplicate product ID: {product_id}")

        seen_ids.add(product_id)

        # Check category
        if product["category"] not in valid_categories:
            raise ValueError(
                f"Invalid category in product {product_id}."
            )

        # Check price
        price = product["price"]

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise ValueError(f"Invalid price in product {product_id}.")

        if price <= 0:
            raise ValueError(f"Price must be positive in {product_id}.")

        # Check currency
        if product["currency"] != "INR":
            raise ValueError(f"Unexpected currency in {product_id}.")

        # Check tag fields
        for tag_field in ["emotional_tags", "interest_tags", "theme_tags"]:
            tags = product[tag_field]

            if not isinstance(tags, list):
                raise ValueError(
                    f"{tag_field} must be a list in {product_id}."
                )

            if not all(isinstance(tag, str) for tag in tags):
                raise ValueError(
                    f"Invalid tag in {product_id}: {tag_field}."
                )

        # Check text and URL fields
        for field in [
            "product_name", "brand", "description",
            "image_url", "product_url"
        ]:
            if not isinstance(product[field], str):
                raise ValueError(
                    f"Invalid value for '{field}' in {product_id}."
                )

    print(f"Validation successful: {len(products)} products checked.")

    return True


def load_products():
    """Load products from the JSON database."""

    if not PRODUCTS_FILE.exists():
        raise FileNotFoundError(
            f"Product database not found: {PRODUCTS_FILE}"
        )

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict) or "products" not in data:
        raise ValueError("JSON must contain a top-level 'products' key.")

    products = data["products"]

    validate_products(products)

    return products
