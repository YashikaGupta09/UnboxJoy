
from database.product_loader import load_products
from recommendation.scoring import calculate_product_score


def get_recommendations(recipient_profile, top_n=10):

    budget = recipient_profile.get("budget_inr")

    if budget is None:
        raise ValueError("Recipient profile must contain budget_inr.")

    if budget <= 0:
        raise ValueError("Budget must be greater than zero.")

    if top_n <= 0:
        raise ValueError("top_n must be greater than zero.")

    products = load_products()

    eligible_products = [
        product for product in products
        if product["price"] <= budget
    ]

    recommendations = []

    for product in eligible_products:
        scores = calculate_product_score(product, recipient_profile)

        recommendations.append({
            "product": product,
            "scores": scores
        })

    # Sort by match score, highest first
    recommendations.sort(
        key=lambda item: item["scores"]["final_score"],
        reverse=True
    )

    # First pass: Select the best product from each category
    diverse_recommendations = []
    selected_categories = set()

    for item in recommendations:
        category = item["product"]["category"]

        if category not in selected_categories:
            diverse_recommendations.append(item)
            selected_categories.add(category)

    # Second pass: Fill remaining positions with highest-scoring products
    selected_ids = {
        item["product"]["product_id"]
        for item in diverse_recommendations
    }

    for item in recommendations:
        if len(diverse_recommendations) >= top_n:
            break

        product_id = item["product"]["product_id"]

        if product_id not in selected_ids:
            diverse_recommendations.append(item)
            selected_ids.add(product_id)

    return diverse_recommendations[:top_n]
