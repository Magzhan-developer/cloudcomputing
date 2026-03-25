/**
 * validationEngine.js
 * Input validation rules per SSOT Section 6.4:
 *   - All inputs must be numeric
 *   - All inputs must be >= 0
 *   - Empty inputs are not allowed
 */

/**
 * Validates a single input value.
 * @param {string} key - The field name.
 * @param {string} rawValue - The raw string value from the input field.
 * @returns {{ valid: boolean, error: string|null }}
 */
export function validateField(key, rawValue) {
  // SSOT 6.4: Empty inputs are not allowed
  if (rawValue === '' || rawValue === null || rawValue === undefined) {
    return { valid: false, error: `${key} is required. Empty inputs are not allowed.` };
  }

  const value = Number(rawValue);

  // SSOT 6.4: All inputs must be numeric
  if (isNaN(value)) {
    return { valid: false, error: `${key} must be numeric.` };
  }

  // SSOT 6.4: All inputs must be >= 0
  if (value < 0) {
    return { valid: false, error: `${key} must be >= 0.` };
  }

  return { valid: true, error: null };
}

/**
 * Validates all input fields.
 * @param {Object} inputs - Key-value map of all input fields (string values).
 * @returns {{ valid: boolean, errors: Object }}
 */
export function validateAllInputs(inputs) {
  const errors = {};
  let allValid = true;

  for (const [key, rawValue] of Object.entries(inputs)) {
    const result = validateField(key, rawValue);
    if (!result.valid) {
      errors[key] = result.error;
      allValid = false;
    }
  }

  return { valid: allValid, errors };
}
