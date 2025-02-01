import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function StockRecommendationApp() {
  const [ticker, setTicker] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [riskLevel, setRiskLevel] = useState('medium');
  const [recommendation, setRecommendation] = useState(null);

  const handleSubmit = async () => {
    const response = await fetch('/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker, start_date: startDate, end_date: endDate, risk_level: riskLevel })
    });
    const data = await response.json();
    setRecommendation(data);
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <Card className="mb-4">
        <CardContent>
          <h2 className="text-xl font-bold mb-2">Stock Recommendation System</h2>
          <Input placeholder="Ticker (e.g., TSLA)" value={ticker} onChange={(e) => setTicker(e.target.value)} className="mb-2" />
          <Input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} className="mb-2" />
          <Input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} className="mb-2" />
          <select value={riskLevel} onChange={(e) => setRiskLevel(e.target.value)} className="mb-2 p-2 rounded">
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
          <Button onClick={handleSubmit}>Get Recommendation</Button>
        </CardContent>
      </Card>

      {recommendation && (
        <Card>
          <CardContent>
            <h3 className="text-lg font-semibold">Recommendation for {recommendation.ticker}</h3>
            <p>Average Return: {(recommendation.average_return * 100).toFixed(2)}%</p>
            <p>Volatility: {(recommendation.volatility * 100).toFixed(2)}%</p>
            <p>{recommendation.manipulated ? '⚠️ Potential Manipulation Detected' : '✅ No Manipulation Detected'}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
