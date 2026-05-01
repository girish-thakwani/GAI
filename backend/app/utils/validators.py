import pandas as pd
from typing import List, Tuple, Optional


REQUIRED_COLUMNS = [
    "date",
    "product_name", 
    "fabric_type",
    "quantity",
    "unit_price",
    "category"
]

VALID_FABRIC_TYPES = [
    "Silk", "Cotton", "Polyester", "Linen", "Wool", "Cashmere",
    "Rayon", "Nylon", "Denim", "Velvet", "Chiffon", "Georgette"
]


def validate_csv_columns(df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
    missing_columns = []
    
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing_columns.append(col)
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    return True, None


def validate_data_types(df: pd.DataFrame) -> Tuple[bool, List[str]]:

    warnings = []
    
    # Check date column
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        try:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            invalid_dates = df['date'].isna().sum()
            if invalid_dates > 0:
                warnings.append(f"{invalid_dates} invalid date(s) found and skipped")
        except Exception:
            return False, ["Invalid date format in 'date' column"]
    
    # Check numeric columns
    if not pd.api.types.is_numeric_dtype(df['quantity']):
        try:
            df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
            df['quantity'] = df['quantity'].fillna(0).clip(lower=0)
        except Exception:
            return False, ["Invalid numeric value in 'quantity' column"]
    
    if not pd.api.types.is_numeric_dtype(df['unit_price']):
        try:
            df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
            df['unit_price'] = df['unit_price'].fillna(0).clip(lower=0)
        except Exception:
            return False, ["Invalid numeric value in 'unit_price' column"]
    
    return True, warnings


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    
    # Create a copy
    df = df.copy()
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Remove rows with invalid dates
    df = df.dropna(subset=['date'])
    
    # Convert numeric columns
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).clip(lower=0)
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce').fillna(0).clip(lower=0)
    
    # Calculate revenue
    df['revenue'] = df['quantity'] * df['unit_price']
    
    # Clean string columns
    df['product_name'] = df['product_name'].astype(str).str.strip()
    df['fabric_type'] = df['fabric_type'].astype(str).str.strip()
    df['category'] = df['category'].astype(str).str.strip()
    
    # Sort by date
    df = df.sort_values('date')
    
    return df