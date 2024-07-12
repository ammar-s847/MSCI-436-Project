from collections import deque

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin

from time_series.garch import (
    train_garch_model, 
    load_garch_model,
    save_garch_model,
)
from time_series.arima import (
    train_arima_model,
    save_arima_model,
)
from time_series.data import (
    fetch_data,
    get_historical_volatility,
    get_implied_volatility,
)
from nlp.news_sentiment import (
    get_company_name, 
    load_news_data, 
    analyze_sentiment,
)

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
socket_app = SocketIO(app, cors_allowed_origins="*")
garch_model = None
arima_model = None
data_queue = None

with open('TICKER.txt', 'r') as file:
    ticker = file.read().strip()

with open('OVERALL_SENTIMENT.txt', 'r') as file:
    overall_sentiment = file.read().strip()

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
    arima_model = train_arima_model(data)
    if not no_save:
        save_garch_model(ticker, garch_model)
        save_arima_model(ticker, arima_model)

def make_stock_decision(
        current_price, 
        arima_prediction, 
        garch_prediction, 
        sentiment_score, 
        holding = False, 
        threshold = 0.02
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

@app.route('/new_ticker', methods=['POST'])
@cross_origin()
def new_ticker():
    data = request.json
    ticker = data['ticker']
    train_ticker(ticker)
    with open('TICKER.txt', 'w') as file:
        file.write(ticker)
    initialize_ticker(ticker)
    return jsonify({"message": f"New ticker {ticker} trained."}), 200

@app.route('/news_sentiment', methods=['GET'])
def news_sentiment():
    news_data = load_news_data(ticker)
    company_name = get_company_name(ticker)
    sentiment_analysis = analyze_sentiment(news_data, ticker, company_name)
    overall_sentiment = sentiment_analysis['overall_sentiment']
    with open('OVERALL_SENTIMENT.txt', 'w') as file:
        file.write(overall_sentiment)
    return jsonify(sentiment_analysis), 200

@app.route('/company_name', methods=['GET'])
def company_name():
    company_name = get_company_name(ticker)
    return jsonify({"company_name": company_name}), 200

@app.route('/volatility', methods=['GET'])
def volatility():
    return jsonify({
        "historical_volatility": get_historical_volatility(ticker),
        "implied_volatility": get_implied_volatility(ticker),
    }), 200

@app.route('/make_decision', methods=['GET'])
def make_decision():
    current_price = fetch_data(ticker).iloc(-1)
    arima_prediction = 100
    garch_prediction = 100
    sentiment_score = overall_sentiment
    holding = False
    
    decision = make_stock_decision(
        current_price, 
        arima_prediction, 
        garch_prediction, 
        sentiment_score, 
        holding
    )
    
    return jsonify({"decision": decision}), 200

@socket_app.on('inference', namespace='/schedule')
def socket_inference(data):
    print(data)
    socket_app.emit('inference', data, namespace='/schedule')

if __name__ == "__main__":
    socket_app.run(app, debug=True, host='127.0.0.1', port=5000)

