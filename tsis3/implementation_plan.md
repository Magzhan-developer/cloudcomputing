# CFO Bot Implementation Plan

This document outlines the architecture, components, and exact formulas required to implement the CFO Bot – Cloud Cost Calculator as per the single source of truth (SSOT).

## Goal Description
Implement a deterministic web-based calculator to estimate the monthly cloud costs for a chatbot application. The application will compute costs based on usage inputs and a selected AI model, providing a breakdown by cloud component and a total monthly estimate. It must run entirely in the browser as a Single Page Application (SPA).

## Project Structure
The application will be built as a modern Single Page Application separated into logic, UI, and configuration/constants, adhering to the standard separation of concerns.

```text
cfo-bot/
├── index.html                   # Entry point
├── src/
│   ├── main.jsx                 # Application root rendering
│   ├── App.jsx                  # Main application layout and state
│   ├── styles/
│   │   └── main.css             # Vanilla CSS, minimalist responsive layout
│   ├── components/
│   │   ├── CalculatorForm.jsx   # Input fields and validation UI
│   │   ├── ModelSelector.jsx    # Model dropdown and selection UI
│   │   └── ResultsDisplay.jsx   # Output formatting (2 decimals, USD)
│   ├── services/
│   │   └── CostEngine.js        # Pure functions mapping directly to SSOT formulas
│   └── utils/
│       ├── validationEngine.js  # Input validation rules
│       └── constants.js         # Pricing models and configurations
```

## Core Components and Services

1. **CalculatorForm (Component)**: Manages numerical inputs (`number_of_users`, `requests_per_user_per_month`, `input_tokens_per_request`, `output_tokens_per_request`, `reads_per_request`, `writes_per_request`, `storage_size_gb`, `data_transfer_gb_per_month`).
2. **ModelSelector (Component)**: Manages selection from predefined AI models (GPT-3.5, GPT-4, Gemini, Claude, Banana Pro) along with associated metadata (`price_per_1k_tokens` and `provider`).
3. **ValidationEngine (Service)**: Validates constraints mapping to Section 6.4 (Inputs must be numeric, >= 0, not empty).
4. **CostEngine (Service)**: Stateless, deterministic calculation module adhering to Section 4 formulas and Section 7 edge cases.
5. **ResultsDisplay (Component)**: Receives computed outputs and displays `Compute_cost`, `AI_cost`, `DB_cost`, `Storage_cost`, `Bandwidth_cost`, and `Total_monthly_cost` with proper UI formatting.

## Required Functions (Cost Engine)
Based strictly on the SSOT, the `CostEngine` will consist of the following deterministic functions:

### Derived Metrics Extractors
- `calculate_requests_per_month(number_of_users, requests_per_user_per_month) -> requests_per_month`
- `calculate_total_input_tokens(input_tokens_per_request, requests_per_month) -> total_input_tokens`
- `calculate_total_output_tokens(output_tokens_per_request, requests_per_month) -> total_output_tokens`
- `calculate_total_tokens(total_input_tokens, total_output_tokens) -> total_tokens`
- `calculate_total_reads(reads_per_request, requests_per_month) -> total_reads`
- `calculate_total_writes(writes_per_request, requests_per_month) -> total_writes`

### Mathematical Cost Models
- `calculate_compute_cost(requests_per_month, cost_per_request)`
  * `requests_per_month * cost_per_request`
  * Edge case: If `requests_per_month = 0`, return `0`
- `calculate_ai_cost(total_tokens, price_per_1k_tokens)`
  * `(total_tokens / 1000) * price_per_1k_tokens`
  * Edge case: If `total_tokens = 0`, return `0`
- `calculate_db_cost(total_reads, cost_per_read, total_writes, cost_per_write)`
  * `(total_reads * cost_per_read) + (total_writes * cost_per_write)`
  * Edge case: If `requests_per_month = 0`, return `0`
- `calculate_storage_cost(storage_size_gb, price_per_gb)`
  * `storage_size_gb * price_per_gb`
- `calculate_bandwidth_cost(data_transfer_gb_per_month, price_per_gb)`
  * `data_transfer_gb_per_month * price_per_gb`
- `calculate_total_monthly_cost(Compute_cost, AI_cost, DB_cost, Storage_cost, Bandwidth_cost)`
  * Sum of all above component costs.

## Data Flow
1. **Input Phase**: User enters parameters into the `CalculatorForm` and selects an AI model from `ModelSelector`.
2. **Event Trigger**: User clicks the "Calculate Cost" button.
3. **Validation**: `ValidationEngine` checks all inputs (e.g. numeric, >= 0, no empty inputs). If validation fails, calculations halt and appropriate errors are displayed inline.
4. **Derived Metrics Phase**: `CostEngine` receives validated inputs and calculates intermediate values (`requests_per_month`, `total_tokens`, `total_reads`, `total_writes`).
5. **Cost Calculation Phase**: `CostEngine` computes individual component costs using the derived metrics and pricing constants (`Constants.js`).
6. **Edge Case Application**: `CostEngine` overrides base formula outputs if specific SSOT rules apply (e.g., setting `AI_cost` to 0 if inputs equal 0, avoiding overflows).
7. **Aggregation Phase**: `CostEngine` calculates the final `Total_monthly_cost`.
8. **Output Phase**: The computed data payload is pushed to `ResultsDisplay` where all variables are converted to strings displaying USD with 2 decimal point precision. The UI updates seamlessly within the < 1 second constraint.
