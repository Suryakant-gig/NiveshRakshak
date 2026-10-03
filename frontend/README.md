# NiveshRakshak — React Frontend (Padmini's Module)

This directory contains the modern React + Vite application for **NIVESHRAKSHAK** (AI-Powered Financial Scam & Misinformation Shield).

---

## 1. Responsibilities & Design System

- **Zero AI Logic**: Presentation layer only. Receives structured JSON from `POST /analyze` or `mockResponse.js` and renders interactive security dashboards.
- **Cybersecurity Aesthetic**: Sleek financial dark mode (`#0B0F19`), crisp typography (Outfit & Inter), radial risk gauge arc visualization, expandable red-flag drawers, and strict claim verification status badges (`SUPPORTED`, `CONTRADICTED`, `UNSUPPORTED`, `UNVERIFIED`).

---

## 2. Component Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Top navbar, disclaimer badge, Mock/Live API mode toggle
│   │   ├── InputPanel.jsx      # Textarea, character counter, load demo preset buttons
│   │   ├── AnalyzeButton.jsx   # Primary glowing action button
│   │   ├── RiskCard.jsx        # Overall risk card with score bars
│   │   ├── RiskGauge.jsx       # Interactive arc radial gauge visualization (0-100)
│   │   ├── RedFlags.jsx        # Interactive expandable red-flag signal cards
│   │   ├── ClaimsAnalysis.jsx  # Extracted claims table with status badges
│   │   ├── EvidencePanel.jsx   # Regulatory & official evidence panel
│   │   ├── ExplanationCard.jsx # "Why was this flagged?" explanation box
│   │   ├── SafeAction.jsx      # "Safe Next Step" security guidance banner
│   │   ├── LoadingState.jsx    # Step-by-step analyzer loading progress animation
│   │   ├── ErrorState.jsx      # Clean error card with "Try Again" CTA
│   │   └── Footer.jsx          # Investor protection footer notice
│   ├── pages/
│   │   ├── Home.jsx            # Input screen page
│   │   └── Results.jsx         # Interactive analysis results page
│   ├── services/
│   │   └── api.js              # Centralized API service (supports mock data & POST /analyze)
│   ├── data/
│   │   └── mockResponse.js     # Prescribed demo case datasets conforming to Section 12 API contract
│   ├── App.jsx                 # Top-level state & flow controller
│   ├── main.jsx                # React DOM root entry
│   └── index.css               # Design system & CSS custom properties
├── package.json
└── vite.config.js
```

---

## 3. Running Locally

```bash
# Install dependencies
npm install

# Start Vite development server (port 3000)
npm run dev
```
