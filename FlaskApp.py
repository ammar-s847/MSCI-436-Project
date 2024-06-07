from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import pickle
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
db = SQLAlchemy(app)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)



def save_model(stock_name, model):
    with open(f'modelstore/{stock_name}_arima.pkl', 'wb') as f:
        pickle.dump(model, f)

def load_model(stock_name):
    with open(f'modelstore/{stock_name}_arima.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

@app.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.json
    stock_name = data.get('name')
    if not stock_name:
        return jsonify({'error': 'Stock name is required'}), 400

    new_stock = Stock(name=stock_name)
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({'message': f'Stock {stock_name} added successfully'}), 201

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    stock_name = data.get('name')
    if not stock_name:
        return jsonify({'error': 'Stock name is required'}), 400

    stock = Stock.query.filter_by(name=stock_name).first()
    if not stock:
        return jsonify({'error': 'Stock not found'}), 404

    stock_data = data.get('data')
    if not stock_data:
        return jsonify({'error': 'Stock data is required'}), 400

    df = pd.DataFrame(stock_data)
    df.columns = ['date', 'price']
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Train ARIMA model
    model = ARIMA(df['price'], order=(5, 1, 0)) # params: num lag observations. num times raw observations are differened, size of moving average window
    model_fit = model.fit()

    # Save model
    save_model(stock_name, model_fit)

    forecast = model_fit.forecast(steps=5)
    return jsonify({'forecast': forecast.tolist()}), 200

if __name__ == '__main__':
    if not os.path.exists('modelstore'):
        os.makedirs('modelstore')
    app.run(debug=True)