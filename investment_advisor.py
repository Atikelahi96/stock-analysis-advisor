import logging
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)

def provide_advice(stock_data):
    logging.info("Calculating investment advice...")
    
    # Calculate the 20-period Simple Moving Average (SMA)
    sma = stock_data['Close'].rolling(window=20).mean().iloc[-1]
    current_price = stock_data['Close'].iloc[-1]
    
    logging.info(f"Latest Close Price: {current_price}, SMA: {sma}")
    
    # Provide investment advice based on SMA and current price
    if current_price > sma:
        logging.info("Advice: Buy")
        return "Buy"
    elif current_price < sma:
        logging.info("Advice: Sell")
        return "Sell"
    else:
        logging.info("Advice: Hold")
        return "Hold"
