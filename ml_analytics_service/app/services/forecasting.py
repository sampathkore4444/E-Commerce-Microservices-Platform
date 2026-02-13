# services/forecasting.py
from datetime import datetime
import pandas as pd
import numpy as np

# In-memory demo storage
forecast_data = {}


def update_forecast(event: dict):
    # Use historical order data to forecast demand
    event_type = event.get("event_type")
    data = event.get("data")

    if event_type == "order_created":
        product_id = data["items"][0]["product_id"]  # simple example
        forecast_data.setdefault(product_id, []).append(
            {"timestamp": datetime.utcnow(), "quantity": data["items"][0]["quantity"]}
        )
        # Simple moving average forecast
        quantities = [d["quantity"] for d in forecast_data[product_id]]
        forecast = np.mean(quantities[-10:])  # last 10 orders
        forecast_data[product_id][-1]["forecast"] = forecast
        print(f"[FORECAST] Product {product_id} forecasted demand: {forecast}")
