import pandas as pd
import numpy as np
import pickle
from collections import deque
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults

def train_arima_model(data) -> ARIMAResults:
    '''Trains a new ARIMA model.'''
    model = ARIMA(data, order=(5, 2, 5))
    model_fit = model.fit()
    print("ARIMA model trained.")
    return model_fit

def forecast_next_value_arima(step: int, model: ARIMAResults) -> np.float64:
    '''Forecasts the next value using ARIMA.'''
    # new_data = pd.Series(queue)
    forecast = model.forecast(steps=step)
    return forecast[0]

def save_arima_model(ticker: str, model: ARIMAResults):
    '''Saves an ARIMA model to disk as a pickle file named based on the ticker.'''
    filename = f'./models/{ticker}_arima_model.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
    print(f"ARIMA model saved to {filename}")

def load_arima_model(ticker: str) -> ARIMAResults:
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
