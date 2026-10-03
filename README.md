# NIVESHRAKSHAK — AI-Powered Financial Scam & Misinformation Shield

**NIVESHRAKSHAK** is an investor-protection shield designed to detect financial scam signals, evaluate claim veracity, and provide clear security guidance.

---

## 1. Project Architecture & Scope

This repository implements the two core modules:

1. **SURYAKANT — AI / Risk Engine (`backend/app/analysis/`)**
   - **Claim Extraction (`claims.py`)**: Deterministic NLP extraction of financial claims (`financial_return`, `regulatory`, etc.).
   - **Scam Signal Detection (`scam_signals.py`)**: Detects observable risk indicators (`GUARANTEED_RETURN`, `UNREALISTIC_RETURN`, `URGENCY`, `LIMITED_TIME`, `PAYMENT_REQUEST`, `FAKE_AUTHORITY`).
   - **Transparent Risk Scoring (`risk_engine.py`)**: Evaluates `scam_score`, `misinformation_score`, and `overall_risk` (`LOW`, `MEDIUM`, `HIGH`). Fully documented in [`risk_methodology.md`](file:///c:/Users/sasha/Downloads/NiveshRakshak/NiveshRakshak/risk_methodology.md).
   - **FastAPI Endpoint (`backend/app/main.py`)**: Exposes `POST /analyze`.

2. **PADMINI — React Frontend (`frontend/`)**
   - Modern React + Vite application with zero AI logic (presentation layer).
   - Interactive financial cybersecurity UI with radial risk gauge, expandable red flag cards, claim verification badges, evidence panel, explanation breakdown, and safe action guidance.

---

## 2. API Contract (Section 12)

Both modules strictly adhere to the frozen JSON schema:

```json
{
  "overall_risk": "HIGH",
  "scam_score": 82,
  "misinformation_score": 71,
  "claims": [
    {
      "id": "claim_001",
      "text": "Guaranteed 30% return in 7 days",
      "type": "financial_return",
      "status": "UNSUPPORTED",
      "reason": "No regulated market product can legally guarantee 30% returns in 7 days."
    }
  ],
  "red_flags": [
    {
      "type": "GUARANTEED_RETURN",
      "severity": "HIGH",
      "label": "Guaranteed return",
      "description": "Promises a guaranteed return, which violates market principles."
    }
  ],
  "evidence": [
    {
      "claim_id": "claim_001",
      "source": "SEBI Investor Advisory Bulletin",
      "text": "SEBI explicitly warns investors against schemes offering guaranteed or fixed returns.",
      "relevance_score": 0.94,
      "url": "https://www.sebi.gov.in"
    }
  ],
  "explanation": "This content contains multiple severe risk signals...",
  "safe_action": "Verify the claim through an authoritative source before taking financial action."
}
```

---

## 3. Quickstart & Verification

### Running Backend API & Unit Tests
```bash
# Set PYTHONPATH and run tests
$env:PYTHONPATH="backend"
python -m pytest tests/

# Run FastAPI backend server (http://localhost:8000)
python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

### Running Frontend Application
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser. Toggle between **Mode: Mock Data** and **Mode: Live API** using the top header button.
