import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)

# --- Configuration ---
N_MONTHS = 12
START_DATE = datetime(2024, 1, 1)

# --- Data Generation ---

def generate_financial_data():
    """Generates synthetic data for Revenue, Cost, and Profit."""
    dates = [START_DATE + timedelta(days=30 * i) for i in range(N_MONTHS)]
    
    # Revenue with an upward trend and seasonality
    base_revenue = np.linspace(500000, 800000, N_MONTHS)
    seasonality = np.sin(np.linspace(0, 2 * np.pi, N_MONTHS)) * 50000
    revenue = (base_revenue + seasonality + np.random.normal(0, 20000, N_MONTHS)).round(2)
    
    # Cost is a percentage of revenue
    cost_of_goods = (revenue * np.random.uniform(0.4, 0.5, N_MONTHS)).round(2)
    
    df = pd.DataFrame({
        'Month': [d.strftime('%Y-%m') for d in dates],
        'Revenue': revenue,
        'Cost_of_Goods': cost_of_goods,
        'Profit': (revenue - cost_of_goods).round(2)
    })
    return df

def generate_marketing_data(financial_df):
    """Generates synthetic data for Marketing KPIs."""
    
    # Marketing Spend (correlated with Revenue)
    marketing_spend = (financial_df['Revenue'] * np.random.uniform(0.05, 0.10, N_MONTHS)).round(2)
    
    # New Customers (correlated with Marketing Spend)
    new_customers = (marketing_spend / np.random.uniform(100, 200, N_MONTHS)).astype(int)
    
    # Customer Churn Rate (inverse correlation with Profit)
    churn_rate = np.clip(0.05 - (financial_df['Profit'] / financial_df['Revenue']) * 0.02, 0.01, 0.10).round(4)
    
    df = pd.DataFrame({
        'Month': financial_df['Month'],
        'Marketing_Spend': marketing_spend,
        'New_Customers': new_customers,
        'Churn_Rate': churn_rate
    })
    return df

# --- Main Execution ---

if __name__ == "__main__":
    # 1. Generate Financial Data
    financial_df = generate_financial_data()
    
    # 2. Generate Marketing Data
    marketing_df = generate_marketing_data(financial_df)
    
    # 3. Merge Data for 360 View
    executive_df = pd.merge(financial_df, marketing_df, on='Month')
    
    # 4. Feature Engineering (KPIs)
    executive_df['Gross_Margin_Pct'] = (executive_df['Profit'] / executive_df['Revenue']).round(4)
    executive_df['CAC'] = (executive_df['Marketing_Spend'] / executive_df['New_Customers']).round(2)
    
    # 5. Load
    executive_df.to_csv('executive_dashboard_data.csv', index=False)
    
    # Save a sample for the README
    executive_df.head().to_markdown('dashboard_data_sample.md')
    
    print("Executive Dashboard Data generated successfully.")
