import yfinance as yf
import pandas as pd

def fetch_data(ticker: str):
    """Fetches 1-minute increment data from Yahoo Finance."""
    stock_data = yf.download(ticker, period="1d", interval="1m")
    return stock_data['Close']

def get_historical_volatility(ticker: str):
    """Fetches the volatility of a stock."""
    stock_data = yf.download(ticker, period="1d", interval="1m")
    stock_data['daily_return'] = stock_data['Close'].pct_change()
    return stock_data['daily_return'].std()

def get_implied_volatility(ticker: str):
    """Fetches the volatility of a stock."""
    stock = yf.Ticker(ticker)
    return stock.option_chain('2022-07-15')['calls']['impliedVolatility'].mean()
