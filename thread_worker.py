import time
import threading
from typing import List

import schedule
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMAResults

from .time_series.arima import load_arima_model

def spawn_workers(tickers: List[str]) -> None:
    for ticker in tickers:
        t = threading.Thread(
            target=thread_worker_function, 
            args=(ticker), 
            daemon=True)
        t.start()

def thread_worker_function(ticker: str):
    loaded = False
    arima_model = load_arima_model(ticker)

    print("starting worker thread for ticker: ", ticker)
    schedule.every(15).minutes.do(track_stock, ticker, arima_model)

    while True:
        schedule.run_pending()
        time.sleep(1)


def track_stock(ticker: str, arima_model: ARIMAResults, load_initial_data: bool) -> None:
    
    prices = []

    data = yf.download(ticker, period="1d", interval="15m")
    current_price = data['Close'].iloc[-1]
    prices.append(current_price)

    if len(prices) > 10:
        prices.pop(0)
        prediction = arima_model.predict(start=len(prices), end=len(prices), dynamic=False)
        print(f"Ticker: {ticker}, Predicted: {prediction[-1]}, Actual: {current_price}")
