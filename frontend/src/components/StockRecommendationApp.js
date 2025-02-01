import React, { useState } from 'react';
import axios from 'axios';

const StockRecommendationApp = () => {
  const [ticker, setTicker] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [riskLevel, setRiskLevel] = useState('medium');
  const [recommendation, setRecommendation] = useState(null);

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/recommend', {
        ticker,
        start_date: startDate,
        end_date: endDate,
        risk_level: riskLevel
      });
      setRecommendation(response.data);
    } catch (error) {
      console.error('Error fetching recommendation', error);
    }
  };

  return (
    <div className="container">
      <h2>Stock Recommendation System</h2>
      <div className="form-group">
        <label>Stock Ticker:</label>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="Enter Stock Ticker"
        />
      </div>
      <div className="form-group">
        <label>Start Date:</label>
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label>End Date:</label>
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label>Risk Level:</label>
        <select
          value={riskLevel}
          onChange={(e) => setRiskLevel(e.target.value)}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>
      <button onClick={handleSubmit}>Get Recommendation</button>

      {recommendation && (
        <div className="result">
          <h3>Recommendation for {recommendation.ticker}</h3>
          <p>Average Return: {(recommendation.average_return * 100).toFixed(2)}%</p>
          <p>Volatility: {(recommendation.volatility * 100).toFixed(2)}%</p>
          <p>
            {recommendation.manipulated
              ? '⚠️ Potential Manipulation Detected'
              : '✅ No Manipulation Detected'}
          </p>
        </div>
      )}
    </div>
  );
};

export default StockRecommendationApp;
