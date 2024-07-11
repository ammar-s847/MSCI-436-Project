import time
import math
from collections import deque
import threading
import socketio

from time_series.garch import (
    forecast_garch,
    load_garch_model,
    train_garch_model,
)
from time_series.arima import (
    forecast_arima,
    load_arima_model,
    train_arima_model,
)
from time_series.data import fetch_data

sio = socketio.Client(engineio_logger=True)

with open('TICKER.txt', 'r') as file:
    ticker = file.read().strip()

port = 5000
host = f'http://127.0.0.1:{port}'
data_queue = None
garch_model = None
garch_pred_queue = deque(maxlen=10)
arima_model = None
arima_pred_queue = deque(maxlen=10)

def initialize_ticker(ticker: str):
    global garch_model, arima_model, data_queue
    data = fetch_data(ticker)
    garch_model = load_garch_model(ticker)
    arima_model = load_arima_model(ticker)
    data_queue = deque(data[-10:], maxlen=10)

def scheduled_inference(ticker: str):
    global data_queue, pred_queue
    new_data = fetch_data(ticker)
    data_queue = deque(new_data[-10:], maxlen=10)

    garch_model = train_garch_model(new_data)
    garch_pred = forecast_garch(data_queue, garch_model)
    garch_pred_queue.append(garch_pred)

    arima_model = train_arima_model(new_data)
    arima_pred = forecast_arima(data_queue, arima_model)
    arima_pred_queue.append(arima_pred)
    # arima_pred_queue.append(data_queue[-1] + math.sin(time.time() / 10.0))

def threaded_job():
    while True:
        scheduled_inference(ticker)
        sio.emit('inference', {'garch': garch_pred_queue[-1], 'arima': arima_pred_queue[-1]}, namespace='/schedule')
        time.sleep(60)

if __name__ == "__main__":
    initialize_ticker(ticker)
    sio.connect(host, namespaces=['/schedule'])
    job_thread = threading.Thread(target=threaded_job, daemon=True)
    job_thread.start()
    sio.wait()
