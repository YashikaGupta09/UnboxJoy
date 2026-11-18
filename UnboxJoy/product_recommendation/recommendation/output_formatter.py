
def format_recommendation_output(recipient_profile, recommendations):

    # Prepare recipient profile for Person 4
    formatted_profile = {
        "relationship": recipient_profile.get("relationship", ""),
        "occasion": recipient_profile.get("occasion", ""),
        "budget_inr": recipient_profile.get("budget_inr", 0),
        "emotional_theme": recipient_profile.get("emotional_theme", ""),
        "sensory_preferences": recipient_profile.get(
            "sensory_preferences",
            recipient_profile.get("matching_tags", {}).get("sensory_tags", [])
        ),
        "interests": recipient_profile.get(
            "interests",
            recipient_profile.get("matching_tags", {}).get("interest_tags", [])
        )
    }

    formatted_recommendations = []

    for item in recommendations:

        product = item["product"]
        scores = item["scores"]

        formatted_recommendations.append({
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "brand": product["brand"],
            "category": product["category"],
            "price": product["price"],
            "currency": product["currency"],
            "description": product["description"],
            "image_url": product["image_url"],
            "product_url": product["product_url"],
            "emotional_tags": product["emotional_tags"],
            "interest_tags": product["interest_tags"],
            "match_score": round(scores["final_score"] / 100, 4)
        })

    return {
        "recipient_profile": formatted_profile,
        "recommendations": formatted_recommendations
    }
