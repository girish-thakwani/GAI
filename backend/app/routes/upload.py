from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.data_processor import data_processor
from app.services.forecaster import forecaster

router = APIRouter()


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are accepted"
        )
    
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Process data
        result = data_processor.load_from_content(content_str)
        
        if not result['success']:
            raise HTTPException(
                status_code=400,
                detail=result['message']
            )
        
        # Train forecasting model
        daily_sales = data_processor.get_daily_sales()
        if len(daily_sales) > 0:
            forecaster.train(daily_sales)
        
        return {
            "success": True,
            "message": result['message'],
            "records_processed": result['records_processed']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/status")
async def get_data_status():
    return {
        "is_loaded": data_processor.is_loaded,
        "records": len(data_processor.df) if data_processor.df is not None else 0
    }