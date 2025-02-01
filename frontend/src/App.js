import React, { useState } from "react";

export default function App() {
  const [ticker, setTicker] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [riskLevel, setRiskLevel] = useState("medium");
  const [recommendation, setRecommendation] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setError("");
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
      }),
    });
    const data = await response.json();
    if (data.error) {
      setError(data.error);
      setRecommendation(null);
    } else {
      setRecommendation(data);
    }
  };

  return (
    <div className="container">
      <h1>Stock Recommendation System</h1>
      <div className="form">
        <input
          type="text"
          placeholder="Ticker (e.g., TSLA)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
        />
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
        <select
          value={riskLevel}
          onChange={(e) => setRiskLevel(e.target.value)}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
        <button onClick={handleSubmit}>Get Recommendation</button>
      </div>

      {error && <div className="error">{error}</div>}

      {recommendation && (
        <div className="result">
          <h3>Recommendation for {recommendation.ticker}</h3>
          <p>Average Return: {(recommendation.average_return * 100).toFixed(2)}%</p>
          <p>Volatility: {(recommendation.volatility * 100).toFixed(2)}%</p>
          <p>
            {recommendation.manipulated
              ? "⚠️ Potential Manipulation Detected"
              : "✅ No Manipulation Detected"}
          </p>
        </div>
      )}
    </div>
  );
}
