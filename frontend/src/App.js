import React, { useState } from "react";
import './App.css';

export default function App() {
  const [ticker, setTicker] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [riskLevel, setRiskLevel] = useState("medium");
  const [budget, setBudget] = useState("");  // Budget field for input
  const [recommendation, setRecommendation] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setError("");
    try {
      const response = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ticker,
          start_date: startDate,
          end_date: endDate,
          risk_level: riskLevel,
          budget: parseFloat(budget),  // Convert budget to number
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();

      if (data && data.ticker) {
        setRecommendation(data);
      } else {
        setError("Invalid response from server");
        setRecommendation(null);
      }
    } catch (error) {
      console.error("Error during fetch:", error);
      setError(error.message);
      setRecommendation(null);
    }
  };

  return (
    <div className="container">
      <h1>Stock Recommendation System 📈</h1>
      <div className="form">
        {/* Input fields stacked vertically */}
        <input
          type="text"
          placeholder="Ticker (e.g., TSLA) 📊"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
        />
        
        <input
          type="text"
          placeholder="Enter your Budget (e.g., 10000) 💵"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
        />

        {/* Date inputs with smoother UI */}
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="date-input"
        />
        
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="date-input"
        />

        <select
          value={riskLevel}
          onChange={(e) => setRiskLevel(e.target.value)}
        >
          <option value="low">Low Risk 😌</option>
          <option value="medium">Medium Risk ⚖️</option>
          <option value="high">High Risk ⚡</option>
        </select>
        
        <button onClick={handleSubmit}>Get Recommendation 🚀</button>
      </div>

      {error && <div className="error">{error}</div>}

      {recommendation && (
        <div className="result">
          <h3>Recommendation for {recommendation.ticker} 📊</h3>
          <p>Average Return: {(recommendation.average_return * 100).toFixed(2)}% 📈</p>
          <p>Volatility: {(recommendation.volatility * 100).toFixed(2)}% 🌪️</p>
          <p>
            {recommendation.manipulated
              ? "⚠️ Potential Manipulation Detected"
              : "✅ No Manipulation Detected"}
          </p>
          
          {/* Investment suggestion */}
          <p>{recommendation.investment_suggestion}</p>

          {/* Suggested amount of stocks to buy */}
          {recommendation.suggested_stocks && (
            <p>Recommended Amount of Stocks: {recommendation.suggested_stocks} 📦</p>
          )}
          
          {/* Graph for stock price over time */}
          {recommendation.stock_graph && (
            <div className="stock-graph">
              <img
                src={`data:image/png;base64,${recommendation.stock_graph}`}
                alt="Stock Price Graph"
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}





