import pandas as pd
import numpy as np
import pickle
from collections import deque
import pmdarima as pm

def train_arima_model(data) -> pm.arima.ARIMA:
    '''Trains a new ARIMA model.'''
    model = pm.arima.auto_arima(data, seasonal=False, m=12)
    model.fit(data)
    print("ARIMA model trained.")
    return model

def forecast_arima(data: deque, model: pm.arima.ARIMA) -> np.float64:
    '''Forecasts the next value using ARIMA.'''
    model.update(data[-1])
    forecast = model.predict(n_periods=1)
    return forecast.item()

def save_arima_model(ticker: str, model: pm.arima.ARIMA):
    '''Saves an ARIMA model to disk as a pickle file named based on the ticker.'''
    filename = f'./models/{ticker}_arima_model.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
    print(f"ARIMA model saved to {filename}")

def load_arima_model(ticker: str) -> pm.arima.ARIMA:
    '''Loads an ARIMA model from a pickle file named based on the ticker.'''
    filename = f'./models/{ticker}_arima_model.pkl'
    try:
        with open(filename, 'rb') as f:
            model = pickle.load(f)
        print(f"ARIMA model loaded from {filename}")
        return model
    except FileNotFoundError:
        print(f"No model found for ticker {ticker}")
        return None
