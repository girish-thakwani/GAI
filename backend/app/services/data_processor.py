import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class DataProcessor:
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.is_loaded = False
    
    def load_csv(self, file_path: str) -> Dict:
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Validate columns
            from app.utils.validators import validate_csv_columns, clean_dataframe
            is_valid, error = validate_csv_columns(df)
            
            if not is_valid:
                return {
                    "success": False,
                    "message": error,
                    "records_processed": 0
                }
            
            # Clean data
            self.df = clean_dataframe(df)
            self.is_loaded = True
            
            return {
                "success": True,
                "message": "Data loaded successfully",
                "records_processed": len(self.df)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error loading CSV: {str(e)}",
                "records_processed": 0
            }
    
    def load_from_content(self, content: str) -> Dict:
        try:
            from io import StringIO
            from app.utils.validators import validate_csv_columns, clean_dataframe
            
            # Read from string
            df = pd.read_csv(StringIO(content))
            
            # Validate columns
            is_valid, error = validate_csv_columns(df)
            
            if not is_valid:
                return {
                    "success": False,
                    "message": error,
                    "records_processed": 0
                }
            
            # Clean data
            self.df = clean_dataframe(df)
            self.is_loaded = True
            
            return {
                "success": True,
                "message": "Data loaded successfully",
                "records_processed": len(self.df)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error processing data: {str(e)}",
                "records_processed": 0
            }
    
    def get_summary(self) -> Dict:
        if not self.is_loaded or self.df is None:
            return {
                "total_revenue": 0,
                "total_orders": 0,
                "top_product": "N/A",
                "avg_order_value": 0,
                "period": "No data"
            }
        
        total_revenue = self.df['revenue'].sum()
        total_orders = len(self.df)
        
        # Get top product by revenue
        top_product_df = self.df.groupby('product_name')['revenue'].sum().sort_values(ascending=False)
        top_product = top_product_df.index[0] if len(top_product_df) > 0 else "N/A"
        
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Get date range
        min_date = self.df['date'].min()
        max_date = self.df['date'].max()
        period = f"{min_date.strftime('%b %Y')} - {max_date.strftime('%b %Y')}" if pd.notna(min_date) else "N/A"
        
        return {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "top_product": top_product,
            "avg_order_value": round(avg_order_value, 2),
            "period": period
        }
    
    def get_monthly_trends(self) -> List[Dict]:
        if not self.is_loaded or self.df is None:
            return []
        
        # Group by month
        self.df['month'] = self.df['date'].dt.to_period('M')
        monthly = self.df.groupby('month').agg({
            'revenue': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        monthly['month'] = monthly['month'].astype(str)
        
        return [
            {
                "month": row['month'],
                "revenue": round(row['revenue'], 2),
                "quantity": int(row['quantity'])
            }
            for _, row in monthly.iterrows()
        ]
    
    def get_top_products(self, limit: int = 10) -> List[Dict]:
        if not self.is_loaded or self.df is None:
            return []
        
        top_products = self.df.groupby(['product_name', 'fabric_type']).agg({
            'revenue': 'sum',
            'quantity': 'sum'
        }).reset_index().sort_values('revenue', ascending=False).head(limit)
        
        return [
            {
                "product_name": row['product_name'],
                "revenue": round(row['revenue'], 2),
                "quantity": int(row['quantity']),
                "fabric_type": row['fabric_type']
            }
            for _, row in top_products.iterrows()
        ]
    
    def get_fabric_breakdown(self) -> List[Dict]:
        if not self.is_loaded or self.df is None:
            return []
        
        fabric_data = self.df.groupby('fabric_type').agg({
            'revenue': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        total_revenue = fabric_data['revenue'].sum()
        
        return [
            {
                "fabric_type": row['fabric_type'],
                "revenue": round(row['revenue'], 2),
                "quantity": int(row['quantity']),
                "percentage": round((row['revenue'] / total_revenue * 100) if total_revenue > 0 else 0, 1)
            }
            for _, row in fabric_data.sort_values('revenue', ascending=False).iterrows()
        ]
    
    def get_inventory_alerts(self, days_threshold: int = 10) -> List[Dict]:
        if not self.is_loaded or self.df is None:
            return []
        
        # Get last 30 days of data
        max_date = self.df['date'].max()
        last_30_days = self.df[self.df['date'] >= (max_date - timedelta(days=30))]
        
        if len(last_30_days) == 0:
            return []
        
        # Calculate daily velocity per product
        daily_sales = last_30_days.groupby('product_name').agg({
            'quantity': 'sum',
            'date': 'count'
        }).reset_index()
        
        daily_sales['daily_velocity'] = daily_sales['quantity'] / 30  # Average daily sales
        daily_sales['days_until_stockout'] = np.where(
            daily_sales['daily_velocity'] > 0,
            100 / daily_sales['daily_velocity'],  # Assuming 100 units as baseline
            float('inf')
        )
        
        # Get fabric types
        product_fabrics = self.df.groupby('product_name')['fabric_type'].first().reset_index()
        daily_sales = daily_sales.merge(product_fabrics, on='product_name')
        
        # Filter to critical and warning
        alerts = daily_sales[daily_sales['days_until_stockout'] <= days_threshold].copy()
        
        def get_status(days):
            if days < 5:
                return "critical"
            elif days < 10:
                return "warning"
            return "ok"
        
        alerts['status'] = alerts['days_until_stockout'].apply(get_status)
        
        return [
            {
                "product_name": row['product_name'],
                "fabric_type": row['fabric_type'],
                "current_velocity": round(row['daily_velocity'], 2),
                "days_until_stockout": round(row['days_until_stockout'], 1),
                "status": row['status']
            }
            for _, row in alerts.sort_values('days_until_stockout').iterrows()
        ]
    
    def get_daily_sales(self) -> List[Dict]:
        if not self.is_loaded or self.df is None:
            return []
        
        daily = self.df.groupby(self.df['date'].dt.date).agg({
            'revenue': 'sum'
        }).reset_index()
        
        daily.columns = ['date', 'revenue']
        
        return [
            {
                "date": str(row['date']),
                "revenue": round(row['revenue'], 2)
            }
            for _, row in daily.iterrows()
        ]


# Global instance
data_processor = DataProcessor()