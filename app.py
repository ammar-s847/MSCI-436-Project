from flask import Flask, request, jsonify
import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import pickle

app = Flask(__name__)

@app.route('/train_arima', methods=['POST'])
def train_arima():
    try:
        # Fetch stock data
        data = request.json
        ticker = data['ticker']
        start_date = data['start_date']
        end_date = data['end_date']
        
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        stock_data = stock_data['Close']
        
        # Split data into train and test sets
        train_size = int(len(stock_data) * 0.8)
        train, test = stock_data[:train_size], stock_data[train_size:]
        
        # Hyperparameter tuning
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
        
        # Train final model with best hyperparameters
        final_model = ARIMA(stock_data, order=best_order)
        final_model_fit = final_model.fit()
        
        # Save the model
        model_filename = f'models/{ticker}_arima_model.pkl'
        with open(model_filename, 'wb') as pkl_file:
            pickle.dump(final_model_fit, pkl_file)
        
        # Evaluate the model
        predictions = final_model_fit.forecast(steps=len(test))
        mse = mean_squared_error(test, predictions)
        
        return jsonify({
            'message': 'Model trained and saved successfully',
            'best_order': best_order,
            'mse': mse
        })
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)