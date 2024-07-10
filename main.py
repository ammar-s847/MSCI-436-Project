from collections import deque

from flask import Flask, request, jsonify
from flask_socketio import SocketIO

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
from nlp.news_sentiment import (
    get_company_name, 
    load_news_data, 
    analyze_sentiment,
)

app = Flask(__name__)
socket_app = SocketIO(app)

ticker = 'TSLA'
garch_model = None
data_queue = None
pred_queue = deque(maxlen=10) # queue to store predictions for the last 10 minutes


def scheduled_inference(ticker: str):
    global garch_model, data_queue, pred_queue
    # new_value = fetch_most_recent_data(ticker)
    # print(new_value)
    # data_queue.append(new_value)
    # print(data_queue)
    # garch_pred = forecast_next_value_garch(data_queue, garch_model)
    # pred_queue.append(garch_pred)
    # print(f"GARCH Prediction: {garch_pred}")
    # print(pred_queue)
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

def train_ticker(ticker: str, no_save: bool = False):
    global garch_model
    data = fetch_data(ticker)
    garch_model = train_garch_model(data)
    if not no_save:
        save_garch_model(ticker, garch_model)


@app.route('/new_ticker', methods=['POST'])
def new_ticker():
    data = request.json
    ticker = data['ticker']
    train_ticker(ticker)

@app.route('/time_series_inference', methods=['GET'])
def new_inference():
    scheduled_inference(ticker)
    return jsonify({"garch": pred_queue[-1]}), 200

@app.route('/news_sentiment', methods=['GET'])
def news_sentiment():
    news_data = load_news_data(ticker)
    company_name = get_company_name(ticker)
    sentiment_analysis = analyze_sentiment(news_data, ticker, company_name)
    return jsonify(sentiment_analysis), 200

@app.route('/company_name', methods=['GET'])
def company_name():
    company_name = get_company_name(ticker)
    return jsonify({"company_name": company_name}), 200

@socket_app.on('inference', namespace='/schedule')
def username(data):
    print(data)

if __name__ == "__main__":
    initialize_ticker(ticker)
    socket_app.run(app, debug=True, host='127.0.0.1', port=5000)
