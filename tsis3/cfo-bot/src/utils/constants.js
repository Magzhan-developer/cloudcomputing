/**
 * constants.js
 * Pricing constants and AI model options as defined in the SSOT (Sections 3.1–3.5, 3.2 Model Options).
 * This file is the single source of pricing truth for the CostEngine.
 */

// SSOT 3.1 – Compute (Serverless Execution)
export const COMPUTE_COST_PER_REQUEST = 0.001; // USD

// SSOT 3.3 – Database (Read/Write Operations)
export const DB_COST_PER_READ = 0.000001;  // USD
export const DB_COST_PER_WRITE = 0.00001;  // USD

// SSOT 3.4 – Storage (Persistent Data)
export const STORAGE_PRICE_PER_GB = 0.02; // USD per month

// SSOT 3.5 – Bandwidth (Network Traffic)
export const BANDWIDTH_PRICE_PER_GB = 0.09; // USD

// SSOT 3.2 – AI Model Options
export const AI_MODELS = [
  { name: 'GPT-3.5',         provider: 'OpenAI',      price_per_1k_tokens: 0.002  },
  { name: 'GPT-4',           provider: 'OpenAI',      price_per_1k_tokens: 0.03   },
  { name: 'GPT-4 Turbo',     provider: 'OpenAI',      price_per_1k_tokens: 0.01   },
  { name: 'Claude 3 Haiku',  provider: 'Anthropic',   price_per_1k_tokens: 0.0015 },
  { name: 'Claude 3 Sonnet', provider: 'Anthropic',   price_per_1k_tokens: 0.003  },
  { name: 'Claude 3 Opus',   provider: 'Anthropic',   price_per_1k_tokens: 0.015  },
  { name: 'Gemini 1.0 Pro',  provider: 'Google',      price_per_1k_tokens: 0.002  },
  { name: 'Gemini 1.5 Pro',  provider: 'Google',      price_per_1k_tokens: 0.005  },
  { name: 'Gemini 1.5 Flash',provider: 'Google',      price_per_1k_tokens: 0.001  },
  { name: 'Banana Pro',      provider: 'Banana.dev',  price_per_1k_tokens: 0.004  },
];

// Input field definitions for the CalculatorForm
export const INPUT_FIELDS = [
  { key: 'number_of_users',              label: 'Number of Users',                  placeholder: 'e.g. 1000'  },
  { key: 'requests_per_user_per_month',  label: 'Requests per User per Month',      placeholder: 'e.g. 20'    },
  { key: 'input_tokens_per_request',     label: 'Input Tokens per Request',          placeholder: 'e.g. 250'   },
  { key: 'output_tokens_per_request',    label: 'Output Tokens per Request',         placeholder: 'e.g. 250'   },
  { key: 'reads_per_request',            label: 'Database Reads per Request',        placeholder: 'e.g. 5'     },
  { key: 'writes_per_request',           label: 'Database Writes per Request',       placeholder: 'e.g. 2'     },
  { key: 'storage_size_gb',             label: 'Storage Size (GB)',                 placeholder: 'e.g. 10'    },
  { key: 'data_transfer_gb_per_month',  label: 'Data Transfer (GB/month)',          placeholder: 'e.g. 5'     },
];
