from flask import Flask, request, jsonify
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# Detect Manipulated Stocks (Simple Outlier Detection)
def detect_manipulated_stocks(data):
    data['Daily Change %'] = (data['Close'] - data['Open']) / data['Open'] * 100
    threshold = data['Daily Change %'].std() * 3
    manipulated = data[abs(data['Daily Change %']) > threshold]
    return manipulated

# Stock Recommendation Logic
def recommend_stocks(symbols, start, end):
    recommendations = []
    for symbol in symbols:
        stock_data = yf.download(symbol, start=start, end=end)
        if stock_data.empty:
            continue

        stock_data['Target'] = (stock_data['Close'].shift(-1) > stock_data['Close']).astype(int)
        features = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
        target = stock_data['Target']

        X_train, X_test, y_train, y_test = train_test_split(features[:-1], target[:-1], test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        if accuracy > 0.6:  # Arbitrary threshold for recommendation
            recommendations.append({
                'symbol': symbol,
                'accuracy': accuracy,
                'manipulated': not detect_manipulated_stocks(stock_data).empty
            })

    return recommendations

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    symbols = data.get('symbols', ['AAPL', 'TSLA', 'MSFT', 'GOOGL'])  # Default symbols
    start_date = data.get('start_date', '2015-01-01')
    end_date = data.get('end_date', '2024-12-31')

    recommendations = recommend_stocks(symbols, start_date, end_date)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
