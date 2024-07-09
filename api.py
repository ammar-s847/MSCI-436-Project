from flask import Flask, request, jsonify

from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import pickle

app = Flask(__name__)



@app.route('/load_models', methods=['POST'])
def load_models():
    try:
        # Load the ARIMA model
        data = request.json
        ticker = data['ticker']
        
        model_filename = f'models/{ticker}_arima_model.pkl'
        with open(model_filename, 'rb') as pkl_file:
            model = pickle.load(pkl_file)
        
        return jsonify({'message': 'Model loaded successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)})

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



# -------------------------------------------------------------------------------
import time
import pickle
from flask import Flask, request, jsonify
from multiprocessing import Process, Manager
import yfinance as yf
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
from sklearn.metrics import mean_squared_error

app = Flask(__name__)
manager = Manager()
tracked_stocks = manager.dict()
processes = []

def load_model(ticker):
    with open(f'{ticker}_arima_model.pkl', 'rb') as f:
        model = ARIMAResults.load(f)
    return model

def track_stock(ticker):
    model = load_model(ticker)
    prices = []

    loop_counter = 40

    while loop_counter > 0:
        data = yf.download(ticker, period="1d", interval="15m")
        current_price = data['Close'].iloc[-1]
        prices.append(current_price)
        if len(prices) > 10:
            prices.pop(0)
            prediction = model.predict(start=len(prices), end=len(prices), dynamic=False)
            print(f"Ticker: {ticker}, Predicted: {prediction[-1]}, Actual: {current_price}")
        time.sleep(60)  # sleep for 1 minute
        loop_counter -= 1


@app.route('/track_tickers', methods=['POST'])
def track_tickers():
    tickers = request.json.get('tickers', [])
    for ticker in tickers:
        if ticker not in tracked_stocks:
            p = Process(target=track_stock, args=(ticker,))
            processes.append(p)
            p.start()
            tracked_stocks[ticker] = p
    return jsonify({'status': 'Tracking started for tickers: ' + ', '.join(tickers)}), 200


@app.route('/untrack_tickers', methods=['POST'])
def untrack_tickers():
    tickers = request.json.get('tickers', [])
    for ticker in tickers:
        if ticker in tracked_stocks:
            tracked_stocks[ticker].terminate()
            del tracked_stocks[ticker]
    return jsonify({'status': 'Tracking stopped for tickers: ' + ', '.join(tickers)}), 200


@app.route('/load_tickers', methods=['POST'])
def load_tickers():
    try:
        data = request.json
        ticker = data['ticker']
        
        model_filename = f'models/{ticker}_arima_model.pkl'
        with open(model_filename, 'rb') as pkl_file:
            model = pickle.load(pkl_file)
        
        return jsonify({'message': 'Model loaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


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
    for p in processes:
        p.join()
    app.run(debug=True)