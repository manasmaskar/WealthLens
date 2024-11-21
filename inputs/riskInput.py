def get_risk_profile():
    """
    Function to get the risk profile from the user input.
    
    This function will ensure the user input is converted to lowercase and validated.
    
    Returns:
        str: The validated risk profile ('low', 'medium', 'high').
    """
    # Take user input (user can input any format)
    risk_profile = input("Enter your risk profile (low, medium, high): ").strip().lower()
    
    # Validate input
    if risk_profile not in ['low', 'medium', 'high']:
        raise ValueError("Invalid input! Please enter 'low', 'medium', or 'high'.")
    
    return risk_profile
