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
