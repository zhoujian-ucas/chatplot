import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime, timedelta

def generate_sales_data(num_records: int = 1000) -> pd.DataFrame:
    """Generate sample sales data"""
    np.random.seed(42)
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(num_records)]
    
    # Generate product data
    products = ['Laptop', 'Smartphone', 'Tablet', 'Smartwatch', 'Headphones']
    categories = ['Electronics', 'Mobile', 'Accessories']
    regions = ['North', 'South', 'East', 'West']
    
    data = {
        'date': dates,
        'product': np.random.choice(products, num_records),
        'category': np.random.choice(categories, num_records),
        'region': np.random.choice(regions, num_records),
        'quantity': np.random.randint(1, 50, num_records),
        'unit_price': np.random.uniform(100, 1000, num_records).round(2),
        'customer_satisfaction': np.random.uniform(3, 5, num_records).round(1),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate total sales
    df['total_sales'] = df['quantity'] * df['unit_price']
    
    return df

def generate_weather_data(num_records: int = 1000) -> pd.DataFrame:
    """Generate sample weather data"""
    np.random.seed(42)
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(num_records)]
    
    # Generate weather data
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    weather_conditions = ['Sunny', 'Cloudy', 'Rainy', 'Stormy', 'Snowy']
    
    data = {
        'date': dates,
        'city': np.random.choice(cities, num_records),
        'temperature': np.random.normal(20, 10, num_records).round(1),
        'humidity': np.random.uniform(30, 90, num_records).round(1),
        'precipitation': np.random.exponential(5, num_records).round(2),
        'wind_speed': np.random.uniform(0, 30, num_records).round(1),
        'condition': np.random.choice(weather_conditions, num_records),
    }
    
    return pd.DataFrame(data)

def main():
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent.parent.parent / 'data' / 'sample'
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate and save sales data
    sales_df = generate_sales_data()
    sales_df.to_csv(data_dir / 'sales_data.csv', index=False)
    print(f"Generated sales data: {len(sales_df)} records")
    
    # Generate and save weather data
    weather_df = generate_weather_data()
    weather_df.to_csv(data_dir / 'weather_data.csv', index=False)
    print(f"Generated weather data: {len(weather_df)} records")

if __name__ == "__main__":
    main() 