import React, { useState } from "react";

export default function App() {
  const [ticker, setTicker] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [riskLevel, setRiskLevel] = useState("medium");
  const [budget, setBudget] = useState("");  // Added state for budget
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
          budget: parseFloat(budget), // Ensure budget is sent as a float
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
        <input
          type="number"
          placeholder="Budget (e.g., 5000)"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
        />
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
          <p>Suggested number of stocks: {recommendation.suggested_stocks}</p>
        </div>
      )}
    </div>
  );
}

