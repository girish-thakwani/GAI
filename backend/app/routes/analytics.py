from fastapi import APIRouter, HTTPException
from app.services.data_processor import data_processor

router = APIRouter()


@router.get("/summary")
async def get_summary():
    if not data_processor.is_loaded:
        raise HTTPException(
            status_code=400,
            detail="No data loaded. Please upload a CSV file first."
        )
    
    return data_processor.get_summary()


@router.get("/trends")
async def get_trends():
    if not data_processor.is_loaded:
        raise HTTPException(
            status_code=400,
            detail="No data loaded. Please upload a CSV file first."
        )
    
    return data_processor.get_monthly_trends()


@router.get("/top-products")
async def get_top_products(limit: int = 10):
    if not data_processor.is_loaded:
        raise HTTPException(
            status_code=400,
            detail="No data loaded. Please upload a CSV file first."
        )
    
    return data_processor.get_top_products(limit)


@router.get("/fabric-breakdown")
async def get_fabric_breakdown():
    if not data_processor.is_loaded:
        raise HTTPException(
            status_code=400,
            detail="No data loaded. Please upload a CSV file first."
        )
    
    return data_processor.get_fabric_breakdown()


@router.get("/alerts")
async def get_alerts(days_threshold: int = 10):
    if not data_processor.is_loaded:
        raise HTTPException(
            status_code=400,
            detail="No data loaded. Please upload a CSV file first."
        )
    
    return data_processor.get_inventory_alerts(days_threshold)