import React, { useState } from 'react';
import CalculatorForm from './components/CalculatorForm';
import ModelSelector from './components/ModelSelector';
import ResultsDisplay from './components/ResultsDisplay';
import { validateAllInputs } from './utils/validationEngine';
import { calculateAllCosts } from './services/CostEngine';
import { AI_MODELS, INPUT_FIELDS } from './utils/constants';
import './styles/main.css';

/**
 * App Component
 * Main application layout and state management.
 * Orchestrates data flow: Input → Validation → CostEngine → Display (SSOT Data Flow).
 */

function getInitialInputs() {
  const inputs = {};
  INPUT_FIELDS.forEach((f) => { inputs[f.key] = ''; });
  return inputs;
}

function App() {
  const [inputs, setInputs] = useState(getInitialInputs());
  const [selectedModelIndex, setSelectedModelIndex] = useState(0);
  const [errors, setErrors] = useState({});
  const [results, setResults] = useState(null);

  const handleInputChange = (key, value) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
    // Clear error for this field on change
    if (errors[key]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[key];
        return next;
      });
    }
  };

  const handleCalculate = () => {
    // Step 1: Validation (SSOT 6.4)
    const validation = validateAllInputs(inputs);
    if (!validation.valid) {
      setErrors(validation.errors);
      setResults(null);
      return;
    }
    setErrors({});

    // Step 2: Convert to numbers
    const numericInputs = {};
    for (const [key, value] of Object.entries(inputs)) {
      numericInputs[key] = Number(value);
    }

    // Step 3: Calculate (SSOT 4.1–4.6) with selected model price
    const model = AI_MODELS[selectedModelIndex];
    const costResults = calculateAllCosts(numericInputs, model.price_per_1k_tokens);

    // Step 4: Display results
    setResults(costResults);
  };

  const handleReset = () => {
    setInputs(getInitialInputs());
    setSelectedModelIndex(0);
    setErrors({});
    setResults(null);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <div className="logo-area">
            <span className="logo-icon">💰</span>
            <div>
              <h1 className="app-title">CFO Bot</h1>
              <p className="app-subtitle">Cloud Cost Calculator for Chatbot Applications</p>
            </div>
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="layout-grid">
          <div className="input-column">
            <ModelSelector
              selectedModelIndex={selectedModelIndex}
              onModelChange={setSelectedModelIndex}
            />
            <CalculatorForm
              inputs={inputs}
              errors={errors}
              onInputChange={handleInputChange}
              onCalculate={handleCalculate}
              onReset={handleReset}
            />
          </div>
          <div className="output-column">
            <ResultsDisplay results={results} />
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>CFO Bot v1.0 — Dautbekov Magzhan | All prices in USD</p>
      </footer>
    </div>
  );
}

export default App;
