import yfinance as yf
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    risk_level: str
    budget: float  # budget field

class StockRecommendation(BaseModel):
    ticker: str
    average_return: float
    volatility: float
    manipulated: bool
    investment_suggestion: str
    suggested_stocks: int  # Number of stocks suggested
    price_data: List[dict]  # Add price_data field for returning stock data

def detect_manipulation(stock_data):
    try:
        # Rolling window for volume and price change analysis (e.g., 20 days)
        window = 20
        stock_data['Volume Rolling Mean'] = stock_data['Volume'].rolling(window).mean()
        stock_data['Volume Rolling Std'] = stock_data['Volume'].rolling(window).std()
        
        # Calculate Z-score for daily price change
        stock_data['Price Change'] = stock_data['Close'].pct_change().fillna(0)
        stock_data['Price Change Z-score'] = (stock_data['Price Change'] - stock_data['Price Change'].mean()) / stock_data['Price Change'].std()
        
        # Identify high volume spikes and unusual price movements
        abnormal_volume = stock_data['Volume'] > (stock_data['Volume Rolling Mean'] + 2 * stock_data['Volume Rolling Std'])
        abnormal_price_change = np.abs(stock_data['Price Change Z-score']) > 2  # Z-score threshold for abnormal price movement
        
        # Flag manipulation if both conditions are true
        manipulation_detected = (abnormal_volume & abnormal_price_change).any()
        
        return manipulation_detected
    except Exception as e:
        print("Error in manipulation detection:", e)
        return False


def adjust_for_risk(average_return, volatility, risk_level):
    if risk_level == 'low':
        return average_return * 0.8, volatility * 0.8
    elif risk_level == 'medium':
        return average_return, volatility
    else:  # High risk
        return average_return * 1.2, volatility * 1.2

def suggest_investment(average_return, volatility, risk_level):
    if risk_level == 'low' and average_return > 0 and volatility < 0.02:
        return "✅ Low Risk - Invest"
    elif risk_level == 'medium' and average_return > 0:
        return "⚠️ Moderate Risk - Consider"
    elif risk_level == 'high' and average_return > -0.02:
        return "⚡ High Risk - Speculative"
    else:
        return "❌ High Risk - Avoid"

def calculate_suggested_stocks(budget, current_price, risk_level):
    risk_factor = {"low": 0.1, "medium": 0.25, "high": 0.5}
    investable_amount = budget * risk_factor[risk_level]
    return int(investable_amount // current_price)

@app.post("/recommend")
def recommend_stock(request: StockRequest):
    try:
        if not request.ticker:
            raise ValueError("Ticker cannot be empty.")
        if request.start_date >= request.end_date:
            raise ValueError("Start date must be before end date.")

        stock_data = yf.download(request.ticker, start=request.start_date, end=request.end_date)

        if stock_data.empty:
            raise ValueError("No data found for the provided ticker and date range.")

        stock_data['Daily Return'] = stock_data['Close'].pct_change().fillna(0)
        average_return = stock_data['Daily Return'].mean()
        volatility = stock_data['Daily Return'].std()

        manipulated = detect_manipulation(stock_data)
        adjusted_return, adjusted_volatility = adjust_for_risk(average_return, volatility, request.risk_level)
        investment_suggestion = suggest_investment(adjusted_return, adjusted_volatility, request.risk_level)

        current_price = stock_data['Close'].iloc[-1]
        suggested_stocks = calculate_suggested_stocks(request.budget, current_price, request.risk_level)

        # Prepare price data (last 10 entries of 'Close', 'Volume', 'Daily Return')
        price_data = stock_data[['Close', 'Volume', 'Daily Return']].tail(10).to_dict(orient="records")

        return StockRecommendation(
            ticker=request.ticker,
            average_return=adjusted_return,
            volatility=adjusted_volatility,
            manipulated=manipulated,
            investment_suggestion=investment_suggestion,
            suggested_stocks=suggested_stocks,
            price_data=price_data  # Include price data in the response
        )
    except Exception as e:
        print("Error:", e)  # Log the exact error in the console
        return {"error": f"Error fetching recommendation: {str(e)}"}




