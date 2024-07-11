import time
from collections import deque
import threading
import socketio

from time_series.garch import (
    forecast_next_value_garch,
    load_garch_model,
    train_garch_model,
)
from time_series.data import (
    fetch_data,
)

sio = socketio.Client(engineio_logger=True)

with open('TICKER.txt', 'r') as file:
    ticker = file.read().strip()

port = 5000
host = f'http://127.0.0.1:{port}'
garch_model = None
data_queue = None
pred_queue = deque(maxlen=10) # queue to store predictions for the last 10 minutes

def initialize_ticker(ticker: str):
    global garch_model, data_queue
    data = fetch_data(ticker)
    garch_model = load_garch_model(ticker)
    data_queue = deque(data[-10:], maxlen=10)

def scheduled_inference(ticker: str):
    global garch_model, data_queue, pred_queue
    new_value = fetch_most_recent_data(ticker)
    data_queue.append(new_value)
    garch_model = train_garch_model(ticker)
    garch_pred = forecast_next_value_garch(data_queue, garch_model)
    pred_queue.append(garch_pred)


def threaded_job():
    while True:
        scheduled_inference(ticker)
        output = pred_queue[-1]
        sio.emit('inference', {'garch': output}, namespace='/schedule')
        # print('\nSocket Output: ', output, end='\n')
        time.sleep(60)

if __name__ == "__main__":
    initialize_ticker(ticker)
    sio.connect(host, namespaces=['/schedule'])
    job_thread = threading.Thread(target=threaded_job, daemon=True)
    job_thread.start()
    sio.wait()
