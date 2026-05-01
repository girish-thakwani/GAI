import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler


class Forecaster:
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def _create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Time-based features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)
        
        # Lag features (previous days' sales)
        for lag in [1, 2, 3, 7, 14, 30]:
            df[f'lag_{lag}'] = df['revenue'].shift(lag)
        
        # Rolling averages
        for window in [7, 14, 30]:
            df[f'rolling_mean_{window}'] = df['revenue'].rolling(window=window).mean()
            df[f'rolling_std_{window}'] = df['revenue'].rolling(window=window).std()
        
        return df
    
    def _prepare_training_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        # Create features
        df_features = self._create_features(df)
        
        # Drop rows with NaN (due to lag features)
        df_features = df_features.dropna()
        
        # Feature columns
        feature_cols = [
            'day_of_week', 'day_of_month', 'month', 'quarter', 'week_of_year',
            'lag_1', 'lag_2', 'lag_3', 'lag_7', 'lag_14', 'lag_30',
            'rolling_mean_7', 'rolling_mean_14', 'rolling_mean_30',
            'rolling_std_7', 'rolling_std_14', 'rolling_std_30'
        ]
        
        X = df_features[feature_cols].values
        y = df_features['revenue'].values
        
        return X, y
    
    def train(self, daily_sales: List[Dict]) -> bool:

        if len(daily_sales) < 30:
            # Not enough data for training
            return False
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(daily_sales)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Prepare training data
            X, y = self._prepare_training_data(df)
            
            if len(X) < 10:
                return False
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train Random Forest
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_scaled, y)
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Training error: {e}")
            return False
    
    def predict(self, daily_sales: List[Dict], days_ahead: int = 30) -> List[Dict]:
        
        if not self.is_trained or self.model is None:
            # Fallback to simple moving average if not trained
            return self._simple_forecast(daily_sales, days_ahead)
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(daily_sales)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Get last date
            last_date = df['date'].max()
            
            # Create features for future dates
            forecasts = []
            
            # Use last N days for lag features
            recent_data = df.tail(30).copy()
            
            for i in range(1, days_ahead + 1):
                future_date = last_date + timedelta(days=i)
                
                # Create feature row
                features = {
                    'day_of_week': future_date.dayofweek,
                    'day_of_month': future_date.day,
                    'month': future_date.month,
                    'quarter': future_date.quarter,
                    'week_of_year': future_date.isocalendar().week,
                }
                
                # Add lag features from historical data
                for lag in [1, 2, 3, 7, 14, 30]:
                    lag_date = future_date - timedelta(days=lag)
                    lag_value = df[df['date'] == lag_date]['revenue']
                    features[f'lag_{lag}'] = lag_value.values[0] if len(lag_value) > 0 else 0
                
                # Rolling features
                for window in [7, 14, 30]:
                    recent = df[df['date'] >= (future_date - timedelta(days=window))]['revenue']
                    features[f'rolling_mean_{window}'] = recent.mean() if len(recent) > 0 else 0
                    features[f'rolling_std_{window}'] = recent.std() if len(recent) > 0 else 0
                
                # Create feature array
                feature_cols = [
                    'day_of_week', 'day_of_month', 'month', 'quarter', 'week_of_year',
                    'lag_1', 'lag_2', 'lag_3', 'lag_7', 'lag_14', 'lag_30',
                    'rolling_mean_7', 'rolling_mean_14', 'rolling_mean_30',
                    'rolling_std_7', 'rolling_std_14', 'rolling_std_30'
                ]
                
                X_pred = np.array([[features[col] for col in feature_cols]])
                X_pred = self.scaler.transform(X_pred)
                
                # Predict
                prediction = self.model.predict(X_pred)[0]
                
                # Calculate confidence interval (simplified)
                std = df['revenue'].std()
                lower = max(0, prediction - 1.96 * std)
                upper = prediction + 1.96 * std
                
                forecasts.append({
                    "date": future_date.strftime('%Y-%m-%d'),
                    "predicted_revenue": round(prediction, 2),
                    "lower_bound": round(lower, 2),
                    "upper_bound": round(upper, 2),
                    "is_historical": False
                })
            
            return forecasts
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._simple_forecast(daily_sales, days_ahead)
    
    def _simple_forecast(self, daily_sales: List[Dict], days_ahead: int = 30) -> List[Dict]:
    
        if len(daily_sales) < 7:
            # Not enough data, return zeros
            last_date = datetime.now()
        else:
            df = pd.DataFrame(daily_sales)
            df['date'] = pd.to_datetime(df['date'])
            last_date = df['date'].max()
            
            # Calculate average
            avg_revenue = df.tail(14)['revenue'].mean()
            std = df.tail(14)['revenue'].std()
        
        forecasts = []
        for i in range(1, days_ahead + 1):
            future_date = last_date + timedelta(days=i)
            predicted = avg_revenue if len(daily_sales) >= 7 else 0
            margin = std if len(daily_sales) >= 7 else avg_revenue * 0.2
            
            forecasts.append({
                "date": future_date.strftime('%Y-%m-%d'),
                "predicted_revenue": round(predicted, 2),
                "lower_bound": round(max(0, predicted - margin), 2),
                "upper_bound": round(predicted + margin, 2),
                "is_historical": False
            })
        
        return forecasts


# Global instance
forecaster = Forecaster()