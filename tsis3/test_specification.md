# TEST SPECIFICATION - CFO Bot Cloud Cost Calculator

This document details the test scenarios and requirements for the CFO Bot, ensuring compliance with the System Specification (SSOT) version 1.0.

## 1. UNIT TESTS BY COMPONENT

### 1.1 Compute Cost Formula (SSOT 4.1)
- **Test ID**: TC_COMP_01
- **Description**: Verify Compute_cost = requests_per_month * 0.001
- **Input**: requests_per_month = 50,000
- **Expected Result**: Compute_cost = $50.00

### 1.2 AI Model Cost Formula (SSOT 4.2)
- **Test ID**: TC_AI_01 (GPT-3.5)
- **Description**: Verify AI_cost = (total_tokens / 1000) * 0.002
- **Input**: total_tokens = 5,000,000 (e.g. 50k requests * 100 tokens)
- **Expected Result**: AI_cost = $10.00
- **Test ID**: TC_AI_02 (GPT-4)
- **Description**: Verify AI_cost = (total_tokens / 1000) * 0.03
- **Input**: total_tokens = 1,000,000
- **Expected Result**: AI_cost = $30.00

### 1.3 Database Cost Formula (SSOT 4.3)
- **Test ID**: TC_DB_01
- **Description**: Verify DB_cost = (total_reads * 0.000001) + (total_writes * 0.00001)
- **Input**: total_reads = 500,000, total_writes = 100,000
- **Expected Result**: DB_cost = $0.50 + $1.00 = $1.50

### 1.4 Storage Cost Formula (SSOT 4.4)
- **Test ID**: TC_STOR_01
- **Description**: Verify Storage_cost = storage_size_gb * 0.02
- **Input**: storage_size_gb = 10
- **Expected Result**: Storage_cost = $0.20

### 1.5 Bandwidth Cost Formula (SSOT 4.5)
- **Test ID**: TC_BAND_01
- **Description**: Verify Bandwidth_cost = data_transfer_gb_per_month * 0.09
- **Input**: data_transfer_gb_per_month = 5
- **Expected Result**: Bandwidth_cost = $0.45

## 2. INTEGRATION TESTS (FULL SCENARIOS)

### 2.1 Standard Scenario
- **Test ID**: TC_INT_01
- **Inputs**:
    - number_of_users: 1000
    - requests_per_user_per_month: 20
    - input_tokens_per_request: 250
    - output_tokens_per_request: 250
    - reads_per_request: 5
    - writes_per_request: 2
    - storage_size_gb: 10
    - data_transfer_gb_per_month: 5
    - AI Model: GPT-3.5 (0.002/1k)
- **Calculations**:
    - requests_per_month = 20,000
    - total_tokens = 20,000 * 500 = 10,000,000
    - total_reads = 20,000 * 5 = 100,000
    - total_writes = 20,000 * 2 = 40,000
    - Compute_cost = 20,000 * 0.001 = $20.00
    - AI_cost = (10,000,000 / 1000) * 0.002 = $20.00
    - DB_cost = (100,000 * 0.000001) + (40,000 * 0.00001) = 0.10 + 0.40 = $0.50
    - Storage_cost = 10 * 0.02 = $0.20
    - Bandwidth_cost = 5 * 0.09 = $0.45
- **Expected Output**: **$41.15**

## 3. EDGE CASE TESTS (SSOT Section 7)

### 3.1 Zero Values
- **Test ID**: TC_EDGE_01
- **Input**: Any required input set to 0.
- **Expected Output**: Corresponding cost component = $0.00 (SSOT 7.1).
- **Test Case**: All inputs = 0.
- **Expected Result**: Total Monthly Cost = $0.00.

### 3.2 Maximum Load (SSOT 5.4)
- **Test ID**: TC_EDGE_02
- **Input**:
    - number_of_users: 10,000
    - requests_per_user_per_month: 100
    - (Calculated requests_per_month = 1,000,000)
    - input/output tokens: 500 each
    - AI Model: GPT-4 (0.03/1k)
- **Expected Result**: System handles calculation within 1 second without precision loss (SSOT 5.4).

## 4. VALIDATION TESTS (SSOT Section 6.4)

### 4.1 Non-Numeric Input
- **Test ID**: TC_VAL_01
- **Input**: string "abc" in `number_of_users`.
- **Expected Behavior**: Error message "All inputs must be numeric".

### 4.2 Negative Value
- **Test ID**: TC_VAL_02
- **Input**: `-10` in `storage_size_gb`.
- **Expected Behavior**: Error message "All inputs must be >= 0".

### 4.3 Empty Input
- **Test ID**: TC_VAL_03
- **Input**: Leave `requests_per_month` blank.
- **Expected Behavior**: Error message "Empty inputs are not allowed".

## 5. UI/UX REQUIREMENTS COMPLIANCE

| Test ID | Requirement | Success Criteria |
|---------|-------------|------------------|
| TC_UI_01 | Precision | All output values show 2 decimal precision (e.g. $0.00) |
| TC_UI_02 | Responsiveness | Results update immediately after clicking "Calculate Cost" |
| TC_UI_03 | Input Types | Dropdown for AI model selection is present |

---
**END OF TEST SPECIFICATION**
