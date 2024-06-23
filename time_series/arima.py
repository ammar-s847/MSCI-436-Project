import pandas as pd
import numpy as np
from types import Tuple
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
from sklearn.metrics import mean_squared_error
import pickle
import yfinance as yf

def load_arima_model(ticker: str) -> ARIMAResults:
    '''Retrieves a trained ARIMA model from disk.'''
    with open(f'{ticker}_arima_model.pkl', 'rb') as pkl_file:
        model = ARIMAResults.load(pkl_file)
    return model
    

def save_arima_model(ticker: str, model: ARIMAResults) -> None:
    '''Saves a trained ARIMA model to disk.'''
    with open(f'{ticker}_arima_model.pkl', 'wb') as pkl_file:
        pickle.dump(model, pkl_file)


def train_arima_model(ticker: str) -> Tuple[ARIMAResults, float]:
    '''Trains a new ARIMA model for given ticker.'''
    stock_data = yf.download(ticker, period="30d", interval="15m")
    stock_data = stock_data['Close']

    train_size = int(len(stock_data) * 0.8)
    train, test = stock_data[:train_size], stock_data[train_size:]

    best_order = None
    best_mse = float('inf')
    
    for p in range(5):
        for d in range(2):
            for q in range(5):
                try:
                    model = ARIMA(train, order=(p, d, q))
                    model_fit = model.fit()
                    predictions = model_fit.forecast(steps=len(test))
                    mse = mean_squared_error(test, predictions)
                    
                    if mse < best_mse:
                        best_mse = mse
                        best_order = (p, d, q)
                except:
                    continue
    
    final_model = ARIMA(stock_data, order=best_order)
    final_model_fit = final_model.fit()
    
    save_arima_model(ticker, final_model_fit)
    
    predictions = final_model_fit.forecast(steps=len(test))
    mse = mean_squared_error(test, predictions)
    
    return final_model_fit, mse
    