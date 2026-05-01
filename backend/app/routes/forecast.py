from fastapi import APIRouter, HTTPException
from app.services.data_processor import data_processor
from app.services.forecaster import forecaster

router = APIRouter()


@router.get("/forecast")
async def get_forecast(days: int = 30):
    if not data_processor.is_loaded:
        raise HTTPException(
            status_code=400,
            detail="No data loaded. Please upload a CSV file first."
        )
    
    # Get historical data
    daily_sales = data_processor.get_daily_sales()
    
    if len(daily_sales) == 0:
        raise HTTPException(
            status_code=400,
            detail="No sales data available for forecasting."
        )
    
    # Generate forecast
    forecast_data = forecaster.predict(daily_sales, days_ahead=days)
    
    # Combine historical and forecast
    historical = [
        {
            "date": item["date"],
            "predicted_revenue": item["revenue"],
            "lower_bound": item["revenue"],
            "upper_bound": item["revenue"],
            "is_historical": True
        }
        for item in daily_sales
    ]
    
    # Return combined data
    return {
        "historical": historical,
        "forecast": forecast_data,
        "model_used": "Random Forest Regressor" if forecaster.is_trained else "Moving Average"
    }