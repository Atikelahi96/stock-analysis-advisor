# actionable_insights.py
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def generate_actionable_insights(stock_data):
    """
    Generate actionable insights based on the stock's price movement and trend.
    """
    latest_price = stock_data['Close'].iloc[-1]
    previous_price = stock_data['Close'].iloc[-2]  # 12 hours ago
    price_change = latest_price - previous_price
    percentage_change = (price_change / previous_price) * 100

    # Analyze the trend direction
    if percentage_change > 2:
        action = "Buy: The price is experiencing significant upward momentum."
    elif percentage_change < -2:
        action = "Sell: The price is on a downward trend and could continue falling."
    else:
        action = "Hold: The price trend is stable, but monitor for further movement."
    
    logging.info(f"Generated actionable insight: {action}")
    return action
