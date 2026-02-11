# Product Requirements Document (PRD): Kaspi AI Compliance & Contract Review Agent (Project "Iron Shield")

**Date:** 2026-02-12
**Status:** DRAFT
**Owner:** Senior Product Manager, Enterprise Risk & AI
**Target User:** Senior Procurement / Compliance Officers (Kaspi.kz)

---

## 1. Problem Statement

Senior Procurement Officers at Kaspi.kz are currently the sole line of defense against regulatory breaches in vendor contracts. They face a critical "Compliance Bottleneck":
1.  **Personal Liability:** Officers bear personal legal and career risk for errors, forcing them to manually review every line of disparate vendor contracts.
2.  **Regulatory Complexity:** Global vendor terms frequently conflict with the National Bank of Kazakhstan’s strict data sovereignty and banking secrecy laws.
3.  **Tool Failure:** Existing contract AI tools use "black box" keyword matching and provide "informational only" disclaimers, offering zero accountability or defensibility in an audit.

**The Result:** The approval process takes 2-3 weeks, stalling business innovation, while the officer operates under constant fear of a license-revoking mistake. Speed is irrelevant if safety is not guaranteed.

## 2. Job To Be Done (JTBD)

**When** I am reviewing a complex vendor agreement (e.g., Salesforce, AWS) that uses foreign legal standards,
**I want to** immediately identify specific clauses that violate current National Bank of Kazakhstan regulations with citations,
**So I can** reject or redline the contract with absolute legal confidence and zero risk of personal liability for missing a critical nuance.

## 3. User Persona: "The Gatekeeper"

**Name:** Assel Bekova
**Role:** Senior Procurement Officer
**Experience:** 8+ years at Kaspi
**Key Characteristics:**
*   **Risk-Averse:** Prioritizes regulatory safety over deployment speed.
*   **Skeptic:** Does not trust "AI scores" or "probability." Needs proof.
*   **Overwhelmed:** Reviews 10–15 dense legal documents weekly while managing internal stakeholder pressure.
*   **Fear:** Deep anxiety about personal accountability for a data breach or regulatory fine.

## 4. Success Metrics

We will NOT measure "Time to Approve" as a primary metric. Success is defined by **Confidence** and **Defensibility**.

*   **Audit Readiness (Primary):** 100% of AI-flagged risks must include a specific citation to the relevant text in the *Law on Personal Data* or *National Bank Rules*.
*   **Risk Capture Rate:** System must identify 100% of "Critical" regulatory blockers (e.g., data residency violations) found by a human senior reviewer in benchmark tests.
*   **Reduction in Legal Ping-Pong:** Decrease the number of "Clarification Loops" between Procurement and Legal by 40% by providing pre-validated regulatory reasoning.
*   **User Trust Score:** 4.5/5 rating from Officers on the statement: "I would bet my reputation on this finding."

## 5. Functional Requirements

The AI Agent must perform the following core functions:

### 5.1 Ingestion & Contextual Parsing
*   **Requirement:** Ingest PDF/DOCX vendor contracts (up to 200 pages) and specific annexes (Data Processing Agreements, SLAs).
*   **Detail:** Must accurately identify definitions (e.g., "Customer Data") and apply those definitions to subsequent clauses to detect "derived data" loopholes.

### 5.2 Regulatory Knowledge Graph (RKG)
*   **Requirement:** The system must ground all reasoning in a maintained database of:
    *   Law of the Republic of Kazakhstan on Personal Data and their Protection.
    *   Rules on Information Security for Second-Tier Banks (National Bank of Kazakhstan).
    *   Law on Payments and Payment Systems.
    *   Internal Kaspi Risk Policies (v2026).
*   **Constraint:** This RKG must be updated weekly by Legal Ops.

### 5.3 Evidence-Based Risk Reasoning
*   **Requirement:** For every flagged risk, the agent must generate a **Compliance Trace**:
    1.  **The Clause:** *Excerpt of the specific vendor text.*
    2.  **The Violation:** *Citation of the specific Article/Rule violated.*
    3.  **The Reasoning:** *Natural language explanation of WHY it is a violation (e.g., "This clause allows independent use of data, which violates Article X on Banking Secrecy").*

### 5.4 "Red Flag" & "Yellow Flag" Logic
*   **Critical (Red):** Direct violation of banking license requirements (e.g., Data Residency). *Action: Block approval.*
*   **Warning (Yellow):** Deviations from Kaspi standard terms (e.g., Liability Cap < $1M). *Action: Highlight for human judgment.*

### 5.5 Human-in-the-Loop Workflow
*   **Requirement:** The AI **never** auto-approves. It acts as a "Super-Analyst" that prepares the file for the Officer.
*   **Feature:** "Audit Trail Export" — Identify which human user reviewed the AI finding and made the final decision.

## 6. Non-Goals

*   **Auto-Approval:** The system will NOT have the authority to sign or approve contracts.
*   **General Legal Advice:** The system is specialized for *Procurement Compliance* only, not general corporate law or litigation.
*   **Contract Drafting:** The system will review incoming vendor paper, not draft new contracts from scratch.

## 7. Risks & Constraints

### 7.1 Regulatory Hallucination Risk
*   **Risk:** The model invents a regulation or misinterprets a decree.
*   **Mitigation:** Strict RAG (Retrieval-Augmented Generation) pipeline. The model cannot generate a risk flag without retrieving a specific document chunk from the Knowledge Graph.

### 7.2 Data Privacy
*   **Constraint:** Vendor contracts contain confidential info.
*   **Mitigation:** Deployment on **on-premise** or **private cloud** infrastructure only. No data leaves Kaspi's perimeter for model training.

### 7.3 Liability
*   **Constraint:** If the AI misses a clause, who is responsible?
*   **Mitigation:** Clear UX framing: "Assistant" not "Authority." The Officer's digital signature remains the only binding approval.

## 8. Why This Is Different From Existing Tools

| Feature | Generic Contract AI (e.g., Ironclad, DocuSign AI) | **Kaspi "Iron Shield" Agent** |
| :--- | :--- | :--- |
| **Analysis Depth** | Keyword search ("Find Indemnity") | **Semantic Reasoning** ("Does this Indemnity cover GDPR fines?") |
| **Legal Basis** | Global/US Common Law | **Kazakhstan Civil Code & National Bank Rules** |
| **Output** | "Risk Score: High" | **"Violates Article 12.4 by allowing offshore processing"** |
| **Liability** | "Informational Use Only" | **Audit-Grade Traceability** |
| **Context** | Single Clause Analysis | **Cross-referenced (Definitions + Clause + Annex)** |

---

**Approval:**
*   [ ] Chief Risk Officer
*   [ ] Chief Information Officer
*   [ ] Head of Legal
