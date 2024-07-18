from collections import deque

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import psycopg2
from psycopg2 import sql
import uuid

from time_series.garch import (
    train_garch_model, 
    load_garch_model,
    save_garch_model,
)
from time_series.arima import (
    train_arima_model,
    load_arima_model,
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

TICKER_FILEPATH = './metadata/TICKER.txt'
SENTIMENT_FILEPATH = './metadata/OVERALL_SENTIMENT.txt'

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
ticker = None

conn_params = {
    'dbname': 'msci-436-project',
    'user': 'postgres',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    return psycopg2.connect(**conn_params)

with open(TICKER_FILEPATH, 'r') as file:
    ticker = file.read().strip()

with open(SENTIMENT_FILEPATH, 'r') as file:
    overall_sentiment = file.read().strip()

def initialize_ticker(ticker: str):
    global garch_model, data_queue, arima_model
    data = fetch_data(ticker)
    garch_model = load_garch_model(ticker)
    arima_model = load_arima_model(ticker)
    data_queue = deque(data[-10:], maxlen=10)

def train_ticker(ticker: str, no_save: bool = False):
    global garch_model
    data = fetch_data(ticker)
    garch_model = train_garch_model(data)
    arima_model = train_arima_model(data)
    if not no_save:
        save_garch_model(ticker, garch_model)
        save_arima_model(ticker, arima_model)

@app.route('/new_ticker', methods=['POST'])
@cross_origin()
def new_ticker():
    global ticker
    data = request.json
    ticker = data['ticker']
    train_ticker(ticker)
    with open(TICKER_FILEPATH, 'w') as file:
        file.write(ticker)
    initialize_ticker(ticker)
    socket_app.emit('update_ticker', {'data': ticker}, namespace='/schedule')
    return jsonify({"message": f"New ticker {ticker} trained."}), 200

@app.route('/news_sentiment', methods=['GET'])
@cross_origin()
def news_sentiment():
    with open(TICKER_FILEPATH, 'r') as file:
        ticker = file.read().strip()
    news_data = load_news_data(ticker)
    company_name = get_company_name(ticker)
    sentiment_analysis = analyze_sentiment(news_data, ticker, company_name)
    overall_sentiment = sentiment_analysis['overall_sentiment']
    with open(SENTIMENT_FILEPATH, 'w') as file:
        file.write(overall_sentiment)
    return jsonify(sentiment_analysis), 200

@app.route('/company_name', methods=['GET'])
@cross_origin()
def company_name():
    with open(TICKER_FILEPATH, 'r') as file:
        ticker = file.read().strip()
    company_name = get_company_name(ticker)
    return jsonify({"company_name": company_name}), 200

@app.route('/volatility', methods=['GET'])
@cross_origin()
def volatility():
    with open(TICKER_FILEPATH, 'r') as file:
        ticker = file.read().strip()
    return jsonify({
        "historical_volatility": get_historical_volatility(ticker),
        "implied_volatility": get_implied_volatility(ticker),
    }), 200

@app.route('/trade', methods=['POST'])
def create_trade():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = sql.SQL("""
        INSERT INTO trade (id, symbol, price, position, created_at, "user")
        VALUES (%s, %s, %s, %s, %s, %s)
    """)
    
    cur.execute(query, (
        data['id'],
        data['symbol'],
        data['price'],
        data['position'],
        data['created_at'],
        data['user']
    ))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Trade created successfully"}), 201

@app.route('/ticker', methods=['POST'])
def create_ticker():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = sql.SQL("""
        INSERT INTO ticker (name, symbol, created_at)
        VALUES (%s, %s, %s)
    """)
    
    cur.execute(query, (
        data['name'],
        data['symbol'],
        data['created_at'],
    ))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Ticker created successfully"}), 201

@socket_app.on('inference', namespace='/schedule')
def socket_inference(data):
    print(data)
    socket_app.emit('inference', data, namespace='/schedule')

if __name__ == "__main__":
    socket_app.run(app, debug=True, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True)
