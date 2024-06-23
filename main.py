import time
from multiprocessing import Process, Manager

import pickle
from flask import Flask, request, jsonify
from statsmodels.tsa.arima.model import ARIMAResults
import yfinance as yf

from .time_series.arima import (
    load_arima_model, 
    save_arima_model, 
    train_arima_model
)


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
    loop_counter = 40 # TODO: get rid of this

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


@app.route('/track', methods=['POST'])
def track():
    tickers = request.json.get('tickers', [])
    for ticker in tickers:
        if ticker not in tracked_stocks:
            p = Process(target=track_stock, args=(ticker,))
            processes.append(p)
            p.start()
            tracked_stocks[ticker] = p
    return jsonify({'status': 'Tracking started for tickers: ' + ', '.join(tickers)}), 200


@app.route('/untrack', methods=['POST'])
def untrack():
    tickers = request.json.get('tickers', [])
    for ticker in tickers:
        if ticker in tracked_stocks:
            tracked_stocks[ticker].terminate()
            del tracked_stocks[ticker]
    return jsonify({'status': 'Tracking stopped for tickers: ' + ', '.join(tickers)}), 200


@app.route('/load', methods=['POST'])
def load():
    try:
        data = request.json
        ticker = data['ticker']
        
        model_filename = f'models/{ticker}_arima_model.pkl'
        with open(model_filename, 'rb') as pkl_file:
            model = pickle.load(pkl_file)
        
        return jsonify({'message': 'Model loaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)