import os
import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns
from quantify_risk import quantify_risk  # Importing quantify_risk function

# Base path to your data folders
base_path = '../Fetch_data/data'
us_30_folder = os.path.join(base_path, 'US-30')
extra10_folder = os.path.join(base_path, 'Extra10')
dow_jones_file = os.path.join(base_path, 'indices', 'DOW_JONES_2020_2024.csv')

def load_price_data(folder_path):
    """
    Load adjusted close prices from CSV files in a folder and combine them into a single DataFrame.
    """
    price_data = pd.DataFrame()
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
            df = df[['Adj Close']]
            df.columns = [file_name.replace('.csv', '')]  # Use file name as column name
            price_data = pd.concat([price_data, df], axis=1)
    return price_data

# Load data
us_30_data = load_price_data(us_30_folder)
extra10_data = load_price_data(extra10_folder)
dow_jones_data = pd.read_csv(dow_jones_file, parse_dates=['Date'], index_col='Date')
dow_jones_data = dow_jones_data[['Adj Close']].rename(columns={'Adj Close': 'DOW_JONES_2020_2024'})

# Combine all data into a single DataFrame
price_data = pd.concat([us_30_data, extra10_data, dow_jones_data], axis=1)

# Fill any missing values
price_data = price_data.fillna(method='ffill').fillna(method='bfill')

# Step 1: Calculate Expected Returns and Covariance Matrix with Shrinkage
expected_returns = expected_returns.mean_historical_return(price_data)
covariance_matrix = risk_models.CovarianceShrinkage(price_data).ledoit_wolf()

def optimize_portfolio(risk_profile, expected_returns, covariance_matrix, profile_targets):
    """
    Optimize portfolio based on the risk profile and return non-zero weights.
    """
    # Instantiate the Efficient Frontier with expected returns and the covariance matrix
    ef = EfficientFrontier(expected_returns, covariance_matrix)
    
    # Add constraints before setting the objective
    ef.add_constraint(lambda w: w >= 0)  # No short selling
    ef.add_constraint(lambda w: w.sum() == 1)  # Fully invested

    # Set the objective based on the risk profile
    if risk_profile == "low":
        ef.min_volatility()

    elif risk_profile == "medium":
        ef.max_sharpe()

    elif risk_profile == "high":
        ef.max_quadratic_utility()

    else:
        raise ValueError("Invalid risk profile! Choose from 'low', 'medium', or 'high'.")

    # Get the optimized weights and filter out non-zero weights
    optimal_weights = ef.clean_weights()
    non_zero_weights = {asset: weight for asset, weight in optimal_weights.items() if weight > 0}

    # Print the non-zero optimized weights for the selected risk profile
    print(f"Optimized Weights for {risk_profile.capitalize()}-Risk Profile (non-zero only):")
    for asset, weight in non_zero_weights.items():
        print(f"{asset}: {weight:.4f}")

# Main code to run optimization for a specific risk profile
if __name__ == "__main__":
    # Get user input for the desired risk profile
    risk_profile = input("Enter your desired risk profile (low, medium, high): ").strip().lower()
    
    # Get profile-specific risk targets
    profile_targets = quantify_risk(risk_profile)
    
    # Run optimization for the selected risk profile only
    optimize_portfolio(risk_profile, expected_returns, covariance_matrix, profile_targets)
