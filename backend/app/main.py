import yfinance as yf
import pandas as pd
import numpy as np
import random
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Add CORSMiddleware to handle requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now, or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST)
    allow_headers=["*"],  # Allow all headers
)

# Define the input data model that the frontend will send
class StockRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    risk_level: str

# Define the response model
class StockRecommendation(BaseModel):
    ticker: str
    average_return: float
    volatility: float
    manipulated: bool

# Function to fetch stock data and calculate metrics
def get_stock_recommendation(ticker: str, start_date: str, end_date: str, risk_level: str):
    try:
        # Fetch historical stock data using yfinance
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        # Ensure there's enough data
        if len(stock_data) < 2:
            raise ValueError("Insufficient data for analysis")

        # Calculate daily returns
        stock_data['Daily Return'] = stock_data['Adj Close'].pct_change()
        
        # Calculate moving average and volatility for volume and price
        stock_data['Volume MA'] = stock_data['Volume'].rolling(window=20).mean()
        stock_data['Price MA'] = stock_data['Adj Close'].rolling(window=20).mean()

        # Calculate average return and volatility
        average_return = stock_data['Daily Return'].mean()
        volatility = stock_data['Daily Return'].std()

        # Check for manipulation based on volume and price anomalies
        manipulated = detect_manipulation(stock_data)

        # Adjust risk level based on user selection (optional logic for recommendation)
        if risk_level == 'low':
            # Lower risk means lower average return and volatility
            average_return *= 0.8
            volatility *= 0.5
        elif risk_level == 'high':
            # Higher risk means higher average return and volatility
            average_return *= 1.2
            volatility *= 1.5

        return StockRecommendation(
            ticker=ticker,
            average_return=average_return,
            volatility=volatility,
            manipulated=manipulated
        )

    except Exception as e:
        return {"error": str(e)}

# Manipulation detection logic
def detect_manipulation(stock_data: pd.DataFrame) -> bool:
    #Check for volume anomalies
    volume_anomaly = False
    stock_data['Volume Anomaly'] = stock_data['Volume'] > (stock_data['Volume MA'] * 2)
    if stock_data['Volume Anomaly'].sum() > len(stock_data) * 0.1:  # More than 10% of the time
        volume_anomaly = True

    #Check for price spikes or volatility
    price_spike = False
    price_spike_threshold = 0.1  # 10% price spike
    for i in range(1, len(stock_data)):
        if abs(stock_data['Adj Close'][i] - stock_data['Adj Close'][i - 1]) > (stock_data['Adj Close'][i - 1] * price_spike_threshold):
            price_spike = True
            break
    
    #Combined conditions for manipulation detection
    if volume_anomaly or price_spike:
        return True

    return False

# Route to handle stock recommendation requests
@app.post("/recommend", response_model=StockRecommendation)
async def recommend_stock(request: StockRequest):
    try:
        # Extract data from the request
        ticker = request.ticker
        start_date = request.start_date
        end_date = request.end_date
        risk_level = request.risk_level
        
        # Get the recommendation based on the data
        recommendation = get_stock_recommendation(ticker, start_date, end_date, risk_level)
        
        return recommendation

    except Exception as e:
        return {"error": str(e)}


