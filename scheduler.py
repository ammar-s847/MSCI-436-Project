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
sentiment = None
decision_queue = deque(maxlen=10)
garch_model = None
garch_pred_queue = deque(maxlen=10)
arima_model = None
arima_pred_queue = deque(maxlen=10)

def initialize_ticker(ticker: str):
    global garch_model, arima_model, data_queue, sentiment
    data = fetch_data(ticker)
    garch_model = load_garch_model(ticker)
    arima_model = load_arima_model(ticker)
    data_queue = deque(data[-10:], maxlen=10)
    with open('OVERALL_SENTIMENT.txt', 'r') as file:
        sentiment = file.read().strip()

def make_stock_decision(
        current_price: float, 
        arima_prediction: float, 
        garch_prediction: float, 
        sentiment_score: str, 
        holding: bool = False, 
        threshold: float = 0.02
    ):
    buy_threshold = threshold
    sell_threshold = -threshold
    
    average_prediction = (arima_prediction + garch_prediction) / 2
    
    if sentiment_score == 'positive':
        if average_prediction > current_price * (1 + buy_threshold) and not holding:
            return 'buy'
        elif holding and average_prediction < current_price * (1 + sell_threshold):
            return 'sell'
        else:
            return 'hold'
    elif sentiment_score == 'neutral':
        if average_prediction > current_price and not holding:
            return 'buy'
        elif holding and average_prediction < current_price:
            return 'sell'
        else:
            return 'hold'
    elif sentiment_score == 'negative':
        if holding:
            return 'sell'
        else:
            return 'hold'
    else:
        raise ValueError("Invalid sentiment score. It must be 'positive', 'neutral', or 'negative'.")

def scheduled_job(ticker: str):
    global data_queue, pred_queue
    new_data = fetch_data(ticker)
    data_queue = deque(new_data[-10:], maxlen=10)

    garch_model = train_garch_model(new_data)
    garch_pred = forecast_garch(data_queue, garch_model)
    garch_pred_queue.append(garch_pred)

    arima_model = train_arima_model(new_data)
    arima_pred = forecast_arima(data_queue, arima_model)
    arima_pred_queue.append(arima_pred)

    decision = make_stock_decision(
            current_price=data_queue[-1],
            arima_prediction=arima_pred,
            garch_prediction=garch_pred,
            sentiment_score=sentiment,
            holding=True if decision_queue and decision_queue[-1] in ['hold', 'buy'] else False
        )
    decision_queue.append(decision)

@sio.on('update_ticker', namespace='/schedule')
def update_ticker(data):
    global ticker
    ticker = data['data']
    initialize_ticker(ticker)
    print('Updating tracked ticker to ', ticker)

def threaded_worker():
    global data_queue, sentiment, garch_pred_queue, arima_pred_queue
    while True:
        scheduled_job(ticker)
        garch_pred = garch_pred_queue[-1]
        arima_pred = arima_pred_queue[-1]
        decision = decision_queue[-1] if decision_queue else 'hold'
        sio.emit(
            'inference', 
            {
                'garch': garch_pred, 
                'arima': arima_pred,
                'decision': decision
            }, 
            namespace='/schedule'
        )
        time.sleep(60)

if __name__ == "__main__":
    initialize_ticker(ticker)
    sio.connect(host, namespaces=['/schedule'])
    job_thread = threading.Thread(target=threaded_worker, daemon=True)
    job_thread.start()
    sio.wait()
