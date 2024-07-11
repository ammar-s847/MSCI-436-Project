import yfinance as yf
import pandas as pd

def fetch_data(ticker: str):
    """Fetches 1-minute increment data from Yahoo Finance."""
    stock_data = yf.download(ticker, period="1d", interval="1m")
    return stock_data['Close']

def fetch_most_recent_data(ticker: str):
    """Fetches the most recent data from Yahoo Finance."""
    stock_data = yf.download(ticker, period="1d", interval="1m")
    return stock_data['Close'].iloc[-1]
