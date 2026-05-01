from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SalesRecord(BaseModel):
    date: datetime
    product_name: str
    fabric_type: str
    quantity: int = Field(ge=0)
    unit_price: float = Field(ge=0)
    category: str


class SummaryResponse(BaseModel):
    total_revenue: float
    total_orders: int
    top_product: str
    avg_order_value: float
    period: str


class TrendData(BaseModel):
    month: str
    revenue: float
    quantity: int


class ProductData(BaseModel):
    product_name: str
    revenue: float
    quantity: int
    fabric_type: str


class FabricBreakdown(BaseModel):
    fabric_type: str
    revenue: float
    quantity: int
    percentage: float


class ForecastData(BaseModel):
    date: str
    predicted_revenue: float
    lower_bound: float
    upper_bound: float
    is_historical: bool


class InventoryAlert(BaseModel):
    product_name: str
    fabric_type: str
    current_velocity: float
    days_until_stockout: float
    status: str 


class UploadResponse(BaseModel):
    success: bool
    message: str
    records_processed: int
    errors: Optional[List[str]] = None