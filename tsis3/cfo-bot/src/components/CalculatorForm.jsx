import React from 'react';
import { INPUT_FIELDS } from '../utils/constants';

/**
 * CalculatorForm Component
 * Renders all input fields from SSOT Section 6.1.
 * Displays inline validation errors per SSOT Section 6.4.
 */
function CalculatorForm({ inputs, errors, onInputChange, onCalculate, onReset }) {
  return (
    <form
      className="calculator-form"
      onSubmit={(e) => {
        e.preventDefault();
        onCalculate();
      }}
    >
      <h2 className="section-title">
        <span className="section-icon">⚙️</span>
        Usage Assumptions
      </h2>

      <div className="fields-grid">
        {INPUT_FIELDS.map((field) => (
          <div key={field.key} className={`field-group ${errors[field.key] ? 'has-error' : ''}`}>
            <label htmlFor={`input-${field.key}`} className="field-label">
              {field.label}
            </label>
            <input
              id={`input-${field.key}`}
              type="text"
              className="field-input"
              placeholder={field.placeholder}
              value={inputs[field.key]}
              onChange={(e) => onInputChange(field.key, e.target.value)}
              autoComplete="off"
            />
            {errors[field.key] && (
              <span className="field-error">{errors[field.key]}</span>
            )}
          </div>
        ))}
      </div>

      <div className="form-actions">
        <button type="submit" id="calculate-btn" className="btn btn-primary">
          Calculate Cost
        </button>
        <button type="button" id="reset-btn" className="btn btn-secondary" onClick={onReset}>
          Reset
        </button>
      </div>
    </form>
  );
}

export default CalculatorForm;
