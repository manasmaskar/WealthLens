# Import the get_risk_profile function from riskInput.py
from riskInput import get_risk_profile

def quantify_risk(risk_level):
    """
    Quantifies the risk level by defining target metrics for volatility, maximum drawdown, and Sharpe Ratio.
    
    Parameters:
    - risk_level (str): The risk profile - "low", "medium", or "high".

    Returns:
    - dict: A dictionary containing the target metrics for volatility, drawdown, and Sharpe Ratio.
    """
    # Define risk targets based on the risk level
    risk_targets = {
        'low': {
            'volatility_target': 0.10,     # Max 10% annualized volatility
            'drawdown_limit': 0.15,        # Max 15% drawdown
            'sharpe_ratio_target': 1.5     # Target Sharpe Ratio of at least 1.0
        },
        'medium': {
            'volatility_target': 0.30,     # Max 15% annualized volatility
            'drawdown_limit': 0.2,        # Max 25% drawdown
            'sharpe_ratio_target': 0.8     # Target Sharpe Ratio of at least 0.8
        },
        'high': {
            'volatility_target': 0.40,     # Max 25% annualized volatility
            'drawdown_limit': 0.45,        # Max 35% drawdown
            'sharpe_ratio_target': 0.7     # Target Sharpe Ratio of at least 0.5
        }
    }
    
    # Validate and return the risk targets for the specified risk level
    if risk_level not in risk_targets:
        raise ValueError("Invalid risk level! Please enter 'low', 'medium', or 'high'.")
    
    return risk_targets[risk_level]

# Main function to automatically trigger the process
if __name__ == "__main__":
    try:
        # Automatically trigger get_risk_profile to get user input
        risk_profile = get_risk_profile()
        print(f"Your selected risk profile is: {risk_profile}")
        
        # Pass the user-defined risk profile to quantify_risk
        targets = quantify_risk(risk_profile)
        
        # Print the final results
        print(f"Risk Targets for {risk_profile.capitalize()} Risk Level:")
        print(f" - Volatility Target: {targets['volatility_target'] * 100}%")
        print(f" - Drawdown Limit: {targets['drawdown_limit'] * 100}%")
        print(f" - Sharpe Ratio Target: {targets['sharpe_ratio_target']}")
    
    except ValueError as e:
        print(e)
