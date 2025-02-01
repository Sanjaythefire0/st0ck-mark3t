import yfinance as yf
import pandas as pd
import numpy as np
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

        # Log stock data for debugging
        print(f"Stock Data for {ticker} from {start_date} to {end_date}:")
        print(stock_data.head())  # Inspect first few rows for sanity check

        # Use 'Close' instead of 'Adj Close'
        stock_data['Close'] = stock_data['Close']  # This should already exist

        # Ensure there's enough data
        if len(stock_data) < 2:
            raise ValueError("Insufficient data for analysis")

        # Calculate daily returns on 'Close'
        stock_data['Daily Return'] = stock_data['Close'].pct_change()

        # Check if Daily Return column exists
        if 'Daily Return' not in stock_data.columns:
            raise ValueError("Daily Return calculation failed.")

        # Handle NaN values in daily returns
        stock_data['Daily Return'] = stock_data['Daily Return'].fillna(0)

        # Log the first 10 daily returns to confirm calculation
        print(f"First 10 Daily Returns: {stock_data['Daily Return'].head(10)}")

        # Calculate average return and volatility
        average_return = stock_data['Daily Return'].mean()
        volatility = stock_data['Daily Return'].std()

        # Log calculated average return and volatility
        print(f"Calculated Average Return: {average_return}, Volatility: {volatility}")

        # Replace NaN with 0.0
        average_return = 0.0 if pd.isna(average_return) else average_return
        volatility = 0.0 if pd.isna(volatility) else volatility

        # Adjust risk level based on user selection (reintroduce adjustments)
        if risk_level == 'low':
            average_return *= 0.8
            volatility *= 0.5
        elif risk_level == 'high':
            average_return *= 1.2
            volatility *= 1.5

        # Convert to percentage for display
        average_return_percentage = average_return * 100
        volatility_percentage = volatility * 100

        return StockRecommendation(
            ticker=ticker,
            average_return=average_return_percentage,
            volatility=volatility_percentage,
            manipulated=detect_manipulation(stock_data)
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}

# Manipulation detection logic
def detect_manipulation(stock_data: pd.DataFrame) -> bool:
    volume_anomaly = False
    stock_data['Volume Anomaly'] = stock_data['Volume'] > (stock_data['Volume'].rolling(window=20).mean() * 2)
    if stock_data['Volume Anomaly'].sum() > len(stock_data) * 0.1:
        volume_anomaly = True

    price_spike = False
    stock_data['Price Spike'] = stock_data['Close'].pct_change().abs() > 0.1
    if stock_data['Price Spike'].sum() > len(stock_data) * 0.05:
        price_spike = True

    return volume_anomaly or price_spike

@app.post("/recommend", response_model=StockRecommendation)
def recommend_stock(request: StockRequest):
    result = get_stock_recommendation(request.ticker, request.start_date, request.end_date, request.risk_level)
    if isinstance(result, dict) and "error" in result:
        return {"ticker": request.ticker, "average_return": 0.0, "volatility": 0.0, "manipulated": False}
    return result



