/**
 * CostEngine.js
 * Stateless, deterministic calculation module.
 * All formulas map directly to SSOT Section 4 (Mathematical Cost Models).
 * Edge cases follow SSOT Section 7.
 */

import {
  COMPUTE_COST_PER_REQUEST,
  DB_COST_PER_READ,
  DB_COST_PER_WRITE,
  STORAGE_PRICE_PER_GB,
  BANDWIDTH_PRICE_PER_GB,
} from '../utils/constants.js';

// ============================================================
// Derived Metrics (SSOT Section 2.2)
// ============================================================

/** SSOT 2.2: requests_per_month = number_of_users * requests_per_user_per_month */
export function calculateRequestsPerMonth(numberOfUsers, requestsPerUserPerMonth) {
  return numberOfUsers * requestsPerUserPerMonth;
}

/** SSOT 2.2: total_input_tokens = input_tokens_per_request * requests_per_month */
export function calculateTotalInputTokens(inputTokensPerRequest, requestsPerMonth) {
  return inputTokensPerRequest * requestsPerMonth;
}

/** SSOT 2.2: total_output_tokens = output_tokens_per_request * requests_per_month */
export function calculateTotalOutputTokens(outputTokensPerRequest, requestsPerMonth) {
  return outputTokensPerRequest * requestsPerMonth;
}

/** SSOT 2.2: total_tokens = total_input_tokens + total_output_tokens */
export function calculateTotalTokens(totalInputTokens, totalOutputTokens) {
  return totalInputTokens + totalOutputTokens;
}

/** SSOT 2.2: total_reads = reads_per_request * requests_per_month */
export function calculateTotalReads(readsPerRequest, requestsPerMonth) {
  return readsPerRequest * requestsPerMonth;
}

/** SSOT 2.2: total_writes = writes_per_request * requests_per_month */
export function calculateTotalWrites(writesPerRequest, requestsPerMonth) {
  return writesPerRequest * requestsPerMonth;
}

// ============================================================
// Mathematical Cost Models (SSOT Section 4)
// ============================================================

/**
 * SSOT 4.1: Compute_cost = requests_per_month * cost_per_request
 * SSOT 7: If requests_per_month = 0 → Compute_cost = 0
 */
export function calculateComputeCost(requestsPerMonth) {
  if (requestsPerMonth === 0) return 0;
  return requestsPerMonth * COMPUTE_COST_PER_REQUEST;
}

/**
 * SSOT 4.2: AI_cost = (total_tokens / 1000) * price_per_1k_tokens
 * SSOT 7: If total_tokens = 0 → AI_cost = 0
 */
export function calculateAiCost(totalTokens, pricePer1kTokens) {
  if (totalTokens === 0) return 0;
  return (totalTokens / 1000) * pricePer1kTokens;
}

/**
 * SSOT 4.3: DB_cost = (total_reads * cost_per_read) + (total_writes * cost_per_write)
 * SSOT 7: If requests_per_month = 0 → DB_cost = 0
 */
export function calculateDbCost(totalReads, totalWrites) {
  return (totalReads * DB_COST_PER_READ) + (totalWrites * DB_COST_PER_WRITE);
}

/**
 * SSOT 4.4: Storage_cost = storage_size_gb * price_per_gb
 */
export function calculateStorageCost(storageSizeGb) {
  return storageSizeGb * STORAGE_PRICE_PER_GB;
}

/**
 * SSOT 4.5: Bandwidth_cost = data_transfer_gb_per_month * price_per_gb
 */
export function calculateBandwidthCost(dataTransferGbPerMonth) {
  return dataTransferGbPerMonth * BANDWIDTH_PRICE_PER_GB;
}

/**
 * SSOT 4.6: Total_monthly_cost = Compute_cost + AI_cost + DB_cost + Storage_cost + Bandwidth_cost
 */
export function calculateTotalMonthlyCost(computeCost, aiCost, dbCost, storageCost, bandwidthCost) {
  return computeCost + aiCost + dbCost + storageCost + bandwidthCost;
}

// ============================================================
// Full Calculation Pipeline
// ============================================================

/**
 * Runs the complete cost calculation pipeline.
 * @param {Object} inputs - Validated numeric inputs.
 * @param {number} pricePer1kTokens - Price for the selected AI model.
 * @returns {Object} - All derived metrics and cost components.
 */
export function calculateAllCosts(inputs, pricePer1kTokens) {
  // Derived metrics (SSOT 2.2)
  const requestsPerMonth = calculateRequestsPerMonth(inputs.number_of_users, inputs.requests_per_user_per_month);
  const totalInputTokens = calculateTotalInputTokens(inputs.input_tokens_per_request, requestsPerMonth);
  const totalOutputTokens = calculateTotalOutputTokens(inputs.output_tokens_per_request, requestsPerMonth);
  const totalTokens = calculateTotalTokens(totalInputTokens, totalOutputTokens);
  const totalReads = calculateTotalReads(inputs.reads_per_request, requestsPerMonth);
  const totalWrites = calculateTotalWrites(inputs.writes_per_request, requestsPerMonth);

  // Cost models (SSOT 4.1–4.5)
  const computeCost = calculateComputeCost(requestsPerMonth);
  const aiCost = calculateAiCost(totalTokens, pricePer1kTokens);
  const dbCost = calculateDbCost(totalReads, totalWrites);
  const storageCost = calculateStorageCost(inputs.storage_size_gb);
  const bandwidthCost = calculateBandwidthCost(inputs.data_transfer_gb_per_month);

  // Total (SSOT 4.6)
  const totalMonthlyCost = calculateTotalMonthlyCost(computeCost, aiCost, dbCost, storageCost, bandwidthCost);

  return {
    // Derived metrics
    requestsPerMonth,
    totalInputTokens,
    totalOutputTokens,
    totalTokens,
    totalReads,
    totalWrites,
    // Cost components
    computeCost,
    aiCost,
    dbCost,
    storageCost,
    bandwidthCost,
    totalMonthlyCost,
  };
}
