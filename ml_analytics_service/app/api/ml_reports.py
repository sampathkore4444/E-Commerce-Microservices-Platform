# api/ml_reports.py
from fastapi import APIRouter
from app.services.forecasting import forecast_data
from app.services.recommendations import user_history

router = APIRouter()


@router.get("/forecast/{product_id}")
def get_forecast(product_id: int):
    return forecast_data.get(product_id, [])


@router.get("/recommendations/{user_id}")
def get_recommendations(user_id: int):
    return user_history.get(user_id, [])
