import time
import logging
from typing import List

import pickle
import schedule
from flask import Flask, request, jsonify
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMAResults

from time_series.arima import (
    load_arima_model,
    save_arima_model,
    train_arima_model,
)
# from thread_worker import (
#     spawn_workers, 
#     thread_worker_function,
# )


logger = logging.getLogger(__name__)
app = Flask(__name__)

# @app.route('/track', methods=['POST'])
# def track():
#     tickers = request.json.get('tickers', [])
#     for ticker in tickers:
#         if ticker not in tracked_stocks:
#             p = Process(target=track_stock, args=(ticker,))
#             processes.append(p)
#             p.start()
#             tracked_stocks[ticker] = p
#     output = jsonify({'status': 'Tracking started for tickers: ' + ', '.join(tickers)})
#     logger.info(output)
#     return output, 200


# @app.route('/untrack', methods=['POST'])
# def untrack():
#     tickers = request.json.get('tickers', [])
#     for ticker in tickers:
#         if ticker in tracked_stocks:
#             tracked_stocks[ticker].terminate()
#             del tracked_stocks[ticker]
#     return jsonify({'status': 'Tracking stopped for tickers: ' + ', '.join(tickers)}), 200


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
    # logging.basicConfig(filename='main.py', level=logging.INFO)
    # app.run(debug=True)
    ticker = "TSLA"
    # model, mse = train_arima_model(ticker)
    # save_arima_model(ticker, model)
    with open(f'./models/{ticker}_arima_model.pkl', 'rb') as pkl_file:
        arima_model = ARIMAResults.load(pkl_file)
    # arima_model = load_arima_model(ticker)
    predictions = {"timestamp": time.time(), "arima": 0.0}
    loaded = False
    prices = []
    if loaded == False:
        data = yf.download(ticker, period="1d", interval="15m")
        for i in range(10):
            current_price = data['Close'].iloc[-(10-i)]
            prices.append(current_price)
        loaded = True
    print(prices)

    def track_stock(prices):
        global arima_model, ticker, predictions

        data = yf.download(ticker, period="1d", interval="1m")
        current_price = data['Close'].iloc[-1]
        print("current price: ", current_price)
        prices.append(current_price)
        prices.pop(0)
        prediction = arima_model.predict(start=len(prices), end=len(prices), dynamic=False)
        print(f"Ticker: {ticker}, Predicted: {prediction.iloc[-1]}, Actual: {current_price}")
        # predictions = {"timestamp": time.time(), "arima": prediction}

    print("starting worker thread for ticker: ", ticker)
    schedule.every(1).minutes.do(track_stock, prices)

    while True:
        schedule.run_pending()
        time.sleep(1)
