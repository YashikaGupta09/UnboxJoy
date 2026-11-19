
from flask import Flask, request, jsonify

from database.product_loader import load_products
from recommendation.recommender import get_recommendations
from recommendation.output_formatter import format_recommendation_output


app = Flask(__name__)


# 1. Health Check API
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Recommendation service is running."
    }), 200


# 2. Get All Products API
@app.route("/api/products", methods=["GET"])
def get_all_products():
    try:
        products = load_products()

        return jsonify({
            "total_products": len(products),
            "products": products
        }), 200

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


# 3. Generate Recommendations API
@app.route("/api/recommendations", methods=["POST"])
def generate_recommendations():

    try:
        # Receive JSON sent in the POST request
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({
                "error": "Request body must contain valid JSON."
            }), 400

        # Extract recipient profile
        recipient_profile = data.get("recipient_profile")

        if not isinstance(recipient_profile, dict):
            return jsonify({
                "error": "Missing or invalid recipient_profile."
            }), 400

        # Number of recommendations (5 by default)
        top_n = data.get("top_n", 5)

        if isinstance(top_n, bool) or not isinstance(top_n, int) or top_n <= 0:
            return jsonify({
                "error": "top_n must be a positive integer."
            }), 400

        # Generate recommendations using your existing logic
        recommendations = get_recommendations(
            recipient_profile,
            top_n=top_n
        )

        # Format output according to Person 4's contract
        output = format_recommendation_output(
            recipient_profile,
            recommendations
        )

        return jsonify(output), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
