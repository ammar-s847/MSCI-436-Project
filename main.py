from collections import deque

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

from time_series.garch import (
    train_garch_model, 
    load_garch_model,
    save_garch_model,
    forecast_next_value_garch_steps,
)
# from time_series.arima import (
#     load_arima_model,
#     train_arima_model,
#     save_arima_model,
#     forecast_next_value_arima,
# )
from time_series.data import fetch_data
from nlp.news_sentiment import (
    get_company_name, 
    load_news_data, 
    analyze_sentiment,
)

app = Flask(__name__)
CORS(app)
socket_app = SocketIO(app, cors_allowed_origins="*")
garch_model = None
arima_model = None

with open('TICKER.txt', 'r') as file:
    ticker = file.read().strip()

def initialize_ticker(ticker: str):
    global garch_model, data_queue, arima_model
    data = fetch_data(ticker)
    garch_model = load_garch_model(ticker)
    # arima_model = load_arima_model(ticker)
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
    with open('TICKER.txt', 'w') as file:
        file.write(ticker)
    return jsonify({"message": f"New ticker {ticker} trained."}), 200

# steps = 1
# @app.route('/time_series_inference', methods=['GET'])
# def new_inference():
#     global steps
#     steps += 1
#     garch_pred = forecast_next_value_garch_steps(steps, garch_model)
#     print(steps)
#     # arima_pred = forecast_next_value_arima(steps, arima_model)
#     return jsonify({"garch": garch_pred}), 200

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
def socket_inference(data):
    print(data)
    socket_app.emit('inference', data, namespace='/schedule')

if __name__ == "__main__":
    # train_arima_model(ticker)
    initialize_ticker(ticker)
    socket_app.run(app, debug=True, host='127.0.0.1', port=5000)