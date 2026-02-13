# services/recommendations.py
from collections import defaultdict

# In-memory user-item interactions
user_history = defaultdict(list)


def update_user_recommendations(event: dict):
    event_type = event.get("event_type")
    data = event.get("data")

    if event_type == "order_paid":
        user_id = data["user_id"]
        product_ids = [item["product_id"] for item in data["items"]]
        user_history[user_id].extend(product_ids)
        # Simple co-purchase recommendation
        recommendations = set()
        for pid in product_ids:
            for other_user, history in user_history.items():
                if pid in history and other_user != user_id:
                    recommendations.update(history)
        recommendations.difference_update(product_ids)
        print(
            f"[RECOMMEND] User {user_id} recommended products: {list(recommendations)[:5]}"
        )
