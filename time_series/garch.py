import pandas as pd
import numpy as np
import pickle
from collections import deque
from arch import arch_model 

def train_garch_model(data) -> arch_model:
    """Trains a new GARCH model."""
    global garch_model
    garch_model = arch_model(data, vol='Garch', p=1, q=1)
    garch_model = garch_model.fit(disp='off')
    print("GARCH model trained.")
    return garch_model

def forecast_garch(queue: deque, model: arch_model) -> np.float64:
    """Forecasts the next value using GARCH."""
    forecast = model.forecast(horizon=1, start=len(queue)-10)
    return forecast.mean['h.1'].iloc[-1]

def forecast_next_value_garch_steps(steps: int, model: arch_model) -> np.float64:
    """Forecasts the next value using GARCH."""
    forecast = model.forecast(horizon=steps)
    return forecast.mean['h.1'].iloc[-1]

def save_garch_model(ticker: str, garch_model: arch_model):
    """Saves a GARCH model to disk as a pickle file named based on the ticker."""
    filename = f'./models/{ticker}_garch_model.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(garch_model, f)
    print(f"GARCH model saved to {filename}")

def load_garch_model(ticker: str) -> arch_model:
    """Loads a GARCH model from a pickle file named based on the ticker."""
    filename = f'./models/{ticker}_garch_model.pkl'
    try:
        with open(filename, 'rb') as f:
            garch_model = pickle.load(f)
        print(f"GARCH model loaded from {filename}")
        return garch_model
    except FileNotFoundError:
        print(f"No model found for ticker {ticker}")
        return None
