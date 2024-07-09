# import time
# from typing import List

# import pickle
# import schedule
# from flask import Flask, request, jsonify
# import yfinance as yf
# from statsmodels.tsa.arima.model import ARIMAResults

# from time_series.arima import (
#     load_arima_model,
#     save_arima_model,
#     train_arima_model,
# )
# # from thread_worker import (
# #     spawn_workers, 
# #     thread_worker_function,
# # )




# app = Flask(__name__)

# @app.route('/load_stock', methods=['GET'])
# def load_stock():
#     tickers = request.json.get('tickers', [])

# # @app.route('/track', methods=['POST'])
# # def track():
# #     tickers = request.json.get('tickers', [])
# #     for ticker in tickers:
# #         if ticker not in tracked_stocks:
# #             p = Process(target=track_stock, args=(ticker,))
# #             processes.append(p)
# #             p.start()
# #             tracked_stocks[ticker] = p
# #     output = jsonify({'status': 'Tracking started for tickers: ' + ', '.join(tickers)})
# #     logger.info(output)
# #     return output, 200


# # @app.route('/untrack', methods=['POST'])
# # def untrack():
# #     tickers = request.json.get('tickers', [])
# #     for ticker in tickers:
# #         if ticker in tracked_stocks:
# #             tracked_stocks[ticker].terminate()
# #             del tracked_stocks[ticker]
# #     return jsonify({'status': 'Tracking stopped for tickers: ' + ', '.join(tickers)}), 200


# @app.route('/load', methods=['POST'])
# def load():
#     try:
#         data = request.json
#         ticker = data['ticker']
        
#         model_filename = f'models/{ticker}_arima_model.pkl'
#         with open(model_filename, 'rb') as pkl_file:
#             model = pickle.load(pkl_file)
        
#         return jsonify({'message': 'Model loaded successfully'})
#     except Exception as e:
#         return jsonify({'error': str(e)})


# if __name__ == '__main__':
#     # app.run(debug=True)
#     ticker = "TSLA"
#     # model, mse = train_arima_model(ticker)
#     # save_arima_model(ticker, model)
#     with open(f'./models/{ticker}_arima_model.pkl', 'rb') as pkl_file:
#         arima_model = ARIMAResults.load(pkl_file)
#     # arima_model = load_arima_model(ticker)
#     predictions = {"timestamp": time.time(), "arima": 0.0}
#     loaded = False
#     index = 10
#     prices = []

#     if loaded == False:
#         data = yf.download(ticker, period="1d", interval="1m")
#         for i in range(10):
#             current_price = data['Close'].iloc[i]
#             prices.append(current_price)
#         loaded = True

#     def track_stock(prices):
#         global arima_model, ticker, predictions, index

#         data = yf.download(ticker, period="1d", interval="1m")
#         current_price = data['Close'].iloc[index]
#         index += 1
#         print("current price: ", current_price)
#         prices.append(current_price)
#         prices.pop(0)
#         prediction = arima_model.predict(start=0, end=len(prices), dynamic=False)
#         print(f"Ticker: {ticker}, Predicted: {prediction.iloc[-1]}, Actual: {current_price}")
#         # predictions = {"timestamp": time.time(), "arima": prediction}

#     schedule.every(1).minutes.do(track_stock, prices)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)

import time
import threading
from multiprocessing import Process
from collections import deque

import schedule
from flask import Flask, request, jsonify

from time_series.garch import (
    train_garch_model, 
    forecast_next_value_garch,
    load_garch_model,
    save_garch_model,
)
from time_series.data import (
    fetch_data, 
    fetch_most_recent_data,
)


app = Flask(__name__)
garch_model = None
ticker = 'TSLA'
data_queue = None
pred_queue = deque(maxlen=10) # queue to store predictions for the last 10 minutes


def scheduled_inference(ticker: str):
    global garch_model, data_queue, pred_queue
    new_value = fetch_most_recent_data(ticker)
    print(new_value)
    data_queue.append(new_value)
    print(data_queue)
    garch_pred = forecast_next_value_garch(data_queue, garch_model)
    pred_queue.append(garch_pred)
    print(f"GARCH Prediction: {garch_pred}")
    print(pred_queue)

def initialize_ticker(ticker: str):
    global garch_model, data_queue
    data = fetch_data(ticker)
    garch_model = load_garch_model(ticker)
    data_queue = deque(data[-10:], maxlen=10)

def train_ticker(ticker: str):
    global garch_model
    data = fetch_data(ticker)
    garch_model = train_garch_model(data)
    save_garch_model(ticker, garch_model)


@app.route('/new_ticker', methods=['POST'])
def new_ticker():
    data = request.json
    ticker = data['ticker']
    train_ticker(ticker)

@app.route('/new_inference', methods=['GET'])
def new_inference():
    return jsonify({"garch": pred_queue[-1]}), 200


def run_scheduler():
    while True:
        # schedule.run_pending()
        # scheduled_inference(ticker)
        print("scheduled")
        time.sleep(60)

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func, daemon=True)
    job_thread.start()

if __name__ == "__main__":
    # train_ticker(ticker)
    initialize_ticker(ticker)

    try:
        # app.run(debug=True)

        # scheduler_process = Process(target=run_scheduler)

        # schedule.every(1).minutes.do(scheduled_inference, ticker)

        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        # run_scheduler()

        while True:
            # run_threaded(scheduled_inference)
            scheduled_inference(ticker)
            time.sleep(60)
        
    except KeyboardInterrupt:
        print("Interrupted")
        scheduler_thread.join()
    finally:
        print("Exiting")
