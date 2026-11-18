
from config import (
    PRODUCT_CATEGORIES,
    EMOTIONAL_TAGS,
    INTEREST_TAGS,
    TARGET_PRODUCT_COUNT
)


def display_configuration():

    print("\n========== GIFT CONCIERGE ==========")

    print("\nPRODUCT CATEGORIES")

    for category, products in PRODUCT_CATEGORIES.items():
        print(f"\n{category.upper()}")

        for product in products:
            print(" -", product)

    print("\nEMOTIONAL TAGS")
    print(EMOTIONAL_TAGS)

    print("\nINTEREST TAGS")
    print(INTEREST_TAGS)

    print("\nTARGET PRODUCT COUNT:", TARGET_PRODUCT_COUNT)


if __name__ == "__main__":
    display_configuration()
