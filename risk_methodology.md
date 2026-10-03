# NiveshRakshak Risk Engine Scoring Methodology

This document details the deterministic scoring model implemented by **Suryakant** in `backend/app/analysis/risk_engine.py`.

---

## 1. Overview & Core Principles

NiveshRakshak uses a dual-metric transparent risk evaluation architecture:
1. **Scam Score (`scam_score`)**: Measures behavioral risk indicators (e.g. pressure tactics, unrealistic returns, unauthorized authority claims).
2. **Misinformation Score (`misinformation_score`)**: Measures claim assertion veracity and lack of authoritative verification.
3. **Overall Risk Band (`overall_risk`)**: Categorizes aggregate severity into `LOW`, `MEDIUM`, or `HIGH`.

The system is strictly **deterministic**, **explainable**, and **unit-testable**.

---

## 2. Scam Signal Scoring Weights

Observable scam signals are evaluated with fixed severity weights:

| Signal Severity | Weight (Points) | Description / Example |
| :--- | :--- | :--- |
| **HIGH** | **+25** | `GUARANTEED_RETURN`, `UNREALISTIC_RETURN`, `PAYMENT_REQUEST`, `FAKE_AUTHORITY` |
| **MEDIUM** | **+12** | `URGENCY`, `LIMITED_TIME` |
| **LOW** | **+5** | Minor unverified urgency or emotional push |

### Signal Formula
$$\text{scam\_score} = \min\left(100, \sum \text{Signal Weight}\right)$$

---

## 3. Misinformation Scoring Weights

Claims are extracted and evaluated for verification status:

| Verification Status | Misinformation Impact | Rationale |
| :--- | :--- | :--- |
| **CONTRADICTED** | **+25 points** | Claim directly conflicts with established financial laws or empirical evidence. |
| **UNSUPPORTED** | **+20 points** | Claim promises specific non-standard outcomes with zero supporting evidence. |
| **UNVERIFIED** | **+10 points** | Claim lacks official registration proof or needs regulatory check. |
| **SUPPORTED** | **0 points** | Claim matches verified economic principles or official filings. |

### Misinformation Formula
$$\text{misinfo\_points} = \sum \text{Status Points} + (\text{Num Scam Signals} \times 5)$$
$$\text{misinformation\_score} = \min(100, \text{misinfo\_points})$$

---

## 4. Overall Risk Band Classification

The final `overall_risk` is determined by the composite maximum risk score ($\max(\text{scam\_score}, \text{misinformation\_score})$):

| Composite Score Range | Overall Risk Band | Visual Indicator | Action Required |
| :--- | :--- | :--- | :--- |
| **0 – 39** | **LOW** | Green / Emerald | Proceed with standard financial due diligence. |
| **40 – 69** | **MEDIUM** | Amber / Yellow | Exercise caution; verify claims against official portals. |
| **70 – 100** | **HIGH** | Red / Crimson | High risk of fraud or misinformation. Do not send money. |

---

## 5. Transparency & Verification Guarantee

- **No Black Box AI**: Scores are computed directly from observable features.
- **No Financial Advice**: Output strictly guides investor verification, never recommending buy/sell actions.
- **Frozen API Contract**: The output structure is guaranteed to match the Section 12 API schema.
