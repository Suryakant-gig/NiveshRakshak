# Problem Statement: NiveshRakshak

> **Investor Protection Only. Not Investment Advice.**

---

## 1. Executive Summary

With the explosive growth of retail participation in India's financial markets, everyday citizens are increasingly targeted by sophisticated financial scams, unauthorized schemes, and predatory misinformation. 

Individuals receive dozens of unsolicited messages and tips daily across channels like **WhatsApp, Telegram, YouTube, SMS, Instagram, and fraudulent websites**. Retail investors—especially first-time and Tier-2/3 market entrants—are faced with a single, high-stakes question:

$$\text{\bf "Can I trust this?"}$$

Current solutions fail because users either have no quick way to verify claims or are given opaque black-box opinions without evidence. **NiveshRakshak** solves this problem by providing an explainable, evidence-grounded AI shield that dissects incoming financial messages, detects observable scam signals, verifies factual claims against authoritative regulatory sources, and provides concrete safe next steps.

---

## 2. The Core Problem & Landscape

### 2.1 Pervasive Threat Vectors
1. **Guaranteed Returns on Market Instruments**: Fraudulent entities lure victims by promising fixed, risk-free returns (e.g., *"Invest ₹10,000 today and get guaranteed 30% in 7 days"*). In reality, Indian securities regulations strictly prohibit market intermediaries from guaranteeing equity/derivative returns.
2. **Impersonation & Fake Regulatory Endorsement**: Scammers forge SEBI registration numbers, RBI circulars, or claim *"Govt/SEBI approved scheme"* to manufacture credibility.
3. **Psychological Exploitation (Scarcity & Urgency)**: High-pressure tactics such as *"Limited slots available"*, *"Only 3 spots left"*, and *"Offer expires in 1 hour"* manipulate fear-of-missing-out (FOMO) to bypass critical thinking.
4. **Unregulated Payment Channels**: Soliciting direct money transfers via personal UPI handles, QR codes, or private Telegram channels without verified escrow or registered merchant accounts.
5. **Viral Misinformation & Deceptive Claims**: Spurious financial news, bogus corporate actions, or fabricated dividend announcements spread unchecked across social groups.

### 2.2 Why Existing Approaches Fail
- **Generic LLM Hallucinations**: Prompting a raw LLM with *"Is this a scam?"* produces subjective, inconsistent, and ungrounded answers prone to false positives and confident hallucinations.
- **High Friction in Official Verification**: Navigating SEBI's intermediary database or regulatory circulars is complex, slow, and inaccessible to non-expert users.
- **The "Unverified vs False" Trap**: Ambiguous financial claims are often prematurely labeled "FALSE" by blunt fact-checkers, eroding user trust. Ambiguous content must be treated as `UNVERIFIED` until authoritative evidence confirms or contradicts it.

---

## 3. Product Mission & Answering The Core Question

**NiveshRakshak** answers four fundamental questions for any financial message:

1. **What claims are being made?** (Extracting discrete financial and regulatory assertions).
2. **What red flags are present?** (Detecting observable, rule-based scam indicators).
3. **What evidence supports or contradicts those claims?** (Hybrid retrieval over official SEBI/RBI/regulatory corpora).
4. **What should the user verify before acting?** (Actionable, safe next steps without dispensing investment advice).

---

## 4. Scope: What We Build vs. What We Do Not Build

To ensure strict compliance with financial regulations and maintain absolute integrity, the boundaries of NiveshRakshak are explicitly frozen:

| WE ARE BUILDING | WE ARE NOT BUILDING |
| :--- | :--- |
| **Scam Detection** (observable behavioral red flags) | ❌ **Stock Predictor** |
| **Financial Claim Extraction** | ❌ **Buy / Sell Recommendations** |
| **Misinformation Analysis** | ❌ **Investment Advisor** |
| **Hybrid Evidence Retrieval** (BM25 + Vector + Reranking) | ❌ **Portfolio Optimizer** |
| **Authoritative Source Verification** (SEBI / RBI) | ❌ **Trading Bot** |
| **Explainable Risk Assessment** (Scores + Breakdown) | ❌ **Market Forecasting Engine** |

---

## 5. Target User Journey (MVP Scope)

```
[User Pastes Message]
          │
          ▼
┌─────────────────────────┐
│ Ingestion & Clean Text  │
└───────────┬─────────────┘
            ├──────────────────────────┐
            ▼                          ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│ Claim Extraction (3a)   │  │ Scam Signal Detection(3b)│
└───────────┬─────────────┘  └─────────┬───────────────┘
            ▼                          │
┌─────────────────────────┐            │
│ Hybrid Retrieval (RAG)  │            │
└───────────┬─────────────┘            │
            ▼                          │
┌─────────────────────────┐            │
│ Claim Verification      │            │
└───────────┬─────────────┘            │
            └─────────────┬────────────┘
                          ▼
            ┌─────────────────────────┐
            │       Risk Engine       │
            │  (Scam & Misinfo Score) │
            └─────────────┬───────────┘
                          ▼
            ┌─────────────────────────┐
            │   Safety & Guardrails   │
            │ (No advice/predictions) │
            └─────────────┬───────────┘
                          ▼
            ┌─────────────────────────┐
            │   Explainable Report    │
            └─────────────────────────┘
```

### The Canonical Scenario (Definition of Done)
- **Input**:
  > *"Guaranteed 30% return in 7 days. SEBI approved. Send ₹10,000 today."*
- **Output**:
  - **Overall Risk**: `HIGH` (Score: 82–100/100)
  - **Red Flags Detected**:
    - Guaranteed Return (`GUARANTEED_RETURN` - HIGH)
    - Unrealistic Return (`UNREALISTIC_RETURN` - HIGH)
    - Artificial Urgency (`URGENCY` - MEDIUM)
    - Direct Payment Solicitation (`PAYMENT_REQUEST` - HIGH)
    - Fake Authority (`FAKE_AUTHORITY` - HIGH)
  - **Claim Analysis**:
    - *"30% return in 7 days"* $\to$ `UNSUPPORTED`
    - *"SEBI approved"* $\to$ `UNVERIFIED` (No authoritative registration provided)
  - **Evidence**: Authoritative SEBI advisory on unauthorized schemes.
  - **Plain-Language Explanation**: Grounded summary explaining the presence of predatory indicators.
  - **Safe Action**: *"Do not transfer money. Verify any registration number directly on SEBI's official portal (sebi.gov.in) before acting."*

---

## 6. Social Impact & Scalability

- **Protecting Household Savings**: Millions of Indians risk their life savings in unregulated schemes masquerading as legitimate investment opportunities.
- **Empowering Financial Literacy**: By providing transparent rationales and highlighting observable red flags, NiveshRakshak educates users rather than simply issuing a binary verdict.
- **Scalable Architecture**: Built with modular JSON interfaces, allowing the core analysis pipeline to scale seamlessly across text, messaging bot integrations (WhatsApp/Telegram), browser extensions, and multi-lingual Indian regional languages in future phases.
