import yfinance as yf
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def fetch_stock_data(ticker: str):
    logging.info(f"Fetching data for {ticker}...")
    stock = yf.Ticker(ticker)
    data = stock.history(period="7d", interval="1h")  # Data for the last 7 days at 1-hour intervals
    logging.info(f"Fetched {len(data)} rows of data for {ticker}")
    return data
