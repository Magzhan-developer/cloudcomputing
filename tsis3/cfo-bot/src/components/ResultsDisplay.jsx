import React from 'react';

/**
 * ResultsDisplay Component
 * Displays cost breakdown and total monthly cost.
 * All values in USD with 2 decimal precision (SSOT 6.3).
 */

const COST_ITEMS = [
  { key: 'computeCost',   label: 'Compute Cost',   icon: '🖥️', description: 'Serverless execution' },
  { key: 'aiCost',        label: 'AI Model Cost',   icon: '🤖', description: 'LLM token processing' },
  { key: 'dbCost',        label: 'Database Cost',    icon: '🗄️', description: 'Read/Write operations' },
  { key: 'storageCost',   label: 'Storage Cost',     icon: '💾', description: 'Persistent data' },
  { key: 'bandwidthCost', label: 'Bandwidth Cost',   icon: '🌐', description: 'Network traffic' },
];

function formatUSD(value) {
  return `$${value.toFixed(2)}`;
}

function ResultsDisplay({ results }) {
  if (!results) {
    return (
      <div className="results-panel results-empty">
        <div className="empty-state">
          <span className="empty-icon">📊</span>
          <p>Enter your usage parameters and click <strong>Calculate Cost</strong> to see the breakdown.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="results-panel results-filled">
      <h2 className="section-title">
        <span className="section-icon">📊</span>
        Cost Breakdown
      </h2>

      <div className="cost-items">
        {COST_ITEMS.map((item) => (
          <div key={item.key} className="cost-item">
            <div className="cost-item-left">
              <span className="cost-icon">{item.icon}</span>
              <div className="cost-label-group">
                <span className="cost-label">{item.label}</span>
                <span className="cost-desc">{item.description}</span>
              </div>
            </div>
            <span className="cost-value" id={`result-${item.key}`}>
              {formatUSD(results[item.key])}
            </span>
          </div>
        ))}
      </div>

      <div className="total-cost-bar">
        <span className="total-label">Total Monthly Cost</span>
        <span className="total-value" id="result-totalMonthlyCost">
          {formatUSD(results.totalMonthlyCost)}
        </span>
      </div>

      <div className="derived-metrics">
        <h3 className="metrics-title">Derived Metrics</h3>
        <div className="metrics-grid">
          <div className="metric">
            <span className="metric-label">Requests/month</span>
            <span className="metric-value">{results.requestsPerMonth.toLocaleString()}</span>
          </div>
          <div className="metric">
            <span className="metric-label">Total Tokens</span>
            <span className="metric-value">{results.totalTokens.toLocaleString()}</span>
          </div>
          <div className="metric">
            <span className="metric-label">Total Reads</span>
            <span className="metric-value">{results.totalReads.toLocaleString()}</span>
          </div>
          <div className="metric">
            <span className="metric-label">Total Writes</span>
            <span className="metric-value">{results.totalWrites.toLocaleString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsDisplay;
