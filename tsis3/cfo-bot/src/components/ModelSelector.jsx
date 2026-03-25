import React from 'react';
import { AI_MODELS } from '../utils/constants';

/**
 * ModelSelector Component
 * Dropdown selection for AI model (SSOT 6.2, 3.2 Model Options).
 * Displays model name, provider, and price per 1k tokens.
 */
function ModelSelector({ selectedModelIndex, onModelChange }) {
  return (
    <div className="model-selector">
      <label htmlFor="ai-model-select" className="field-label">
        AI Model
      </label>
      <select
        id="ai-model-select"
        className="model-dropdown"
        value={selectedModelIndex}
        onChange={(e) => onModelChange(Number(e.target.value))}
      >
        {AI_MODELS.map((model, index) => (
          <option key={model.name} value={index}>
            {model.name} ({model.provider}) — ${model.price_per_1k_tokens}/1k tokens
          </option>
        ))}
      </select>
      <div className="model-info">
        <span className="model-provider-badge">
          {AI_MODELS[selectedModelIndex].provider}
        </span>
        <span className="model-price-tag">
          ${AI_MODELS[selectedModelIndex].price_per_1k_tokens} / 1k tokens
        </span>
      </div>
    </div>
  );
}

export default ModelSelector;
