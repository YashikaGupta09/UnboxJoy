
from config import RECOMMENDATION_WEIGHTS


def calculate_match_score(product_tags, recipient_tags):
    """
    Calculate the percentage of recipient tags
    that are matched by the product.
    """

    if not recipient_tags:
        return 0.0

    product_tags = set(product_tags)
    recipient_tags = set(recipient_tags)

    matching_tags = product_tags.intersection(recipient_tags)

    return len(matching_tags) / len(recipient_tags)


def calculate_sensory_score(product, recipient_profile):
    """Check whether the product category matches sensory preferences."""

    sensory_preferences = (
        recipient_profile["matching_tags"].get("sensory_tags", [])
    )

    if not sensory_preferences:
        return 0.0

    return 1.0 if product["category"] in sensory_preferences else 0.0


def calculate_emotional_score(product, recipient_profile):
    """Calculate emotional tag similarity."""

    recipient_tags = (
        recipient_profile["matching_tags"].get("emotion_tags", [])
    )

    return calculate_match_score(
        product["emotional_tags"],
        recipient_tags
    )


def calculate_interest_score(product, recipient_profile):
    """Calculate interest tag similarity."""

    recipient_tags = (
        recipient_profile["matching_tags"].get("interest_tags", [])
    )

    return calculate_match_score(
        product["interest_tags"],
        recipient_tags
    )


def calculate_theme_score(product, recipient_profile):
    """Check how well the product theme matches the recipient's theme."""

    recipient_theme = recipient_profile.get("emotional_theme")

    if not recipient_theme:
        return 0.0

    return calculate_match_score(
        product["theme_tags"],
        [recipient_theme]
    )


def calculate_product_score(product, recipient_profile):
    """Calculate the final weighted recommendation score."""

    sensory_score = calculate_sensory_score(
        product, recipient_profile
    )

    emotional_score = calculate_emotional_score(
        product, recipient_profile
    )

    interest_score = calculate_interest_score(
        product, recipient_profile
    )

    theme_score = calculate_theme_score(
        product, recipient_profile
    )

    final_score = (
        sensory_score * RECOMMENDATION_WEIGHTS["sensory"]
        + emotional_score * RECOMMENDATION_WEIGHTS["emotional"]
        + interest_score * RECOMMENDATION_WEIGHTS["interest"]
        + theme_score * RECOMMENDATION_WEIGHTS["theme"]
    )

    return {
        "sensory_score": round(sensory_score * 100, 2),
        "emotional_score": round(emotional_score * 100, 2),
        "interest_score": round(interest_score * 100, 2),
        "theme_score": round(theme_score * 100, 2),
        "final_score": round(final_score * 100, 2)
    }
