from fastapi import FastAPI, Request
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for user preferences
class StockRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    risk_level: str  # low, medium, high

# Detect manipulated stocks
def detect_manipulation(df):
    model = IsolationForest(contamination=0.01)
    df['returns'] = df['Close'].pct_change()
    df = df.dropna()
    anomalies = model.fit_predict(df[['returns']])
    df['anomaly'] = anomalies
    return df[df['anomaly'] == -1]

# Basic stock recommendation based on historical data
@app.post("/recommend")
async def recommend_stock(req: StockRequest):
    data = yf.download(req.ticker, start=req.start_date, end=req.end_date)
    
    if data.empty:
        return {"error": "No data found for the given ticker."}
    
    manipulated_data = detect_manipulation(data)
    
    recommendation = {
        "ticker": req.ticker,
        "average_return": data['Close'].pct_change().mean(),
        "volatility": data['Close'].pct_change().std(),
        "manipulated": not manipulated_data.empty
    }

    return recommendation

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock Recommendation API!"}
