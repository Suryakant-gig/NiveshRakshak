/**
 * Centralized API Service for NiveshRakshak Frontend.
 * Handles fetching analysis from backend or fallback to mock dataset.
 */
import { MOCK_RESPONSE_CASE_1, DEMO_PRESETS } from '../data/mockResponse';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function analyzeContent(content, useMockData = true) {
  if (!content || !content.strip ? !content.trim() : !content) {
    throw new Error('Input message content cannot be empty.');
  }

  // If Mock Data mode is explicitly enabled
  if (useMockData) {
    // Simulate realistic 800ms API network latency for smooth UI loading experience
    await new Promise(resolve => setTimeout(resolve, 800));

    // Match text against demo cases if matched, or return general mock response
    const contentLower = content.toLowerCase();

    if (contentLower.includes('inflation')) {
      return {
        overall_risk: "LOW",
        scam_score: 5,
        misinformation_score: 0,
        claims: [
          {
            id: "claim_001",
            text: "Inflation reduces the purchasing power of money over time",
            type: "market_claim",
            status: "SUPPORTED",
            reason: "Standard economic principle supported by central bank literature."
          }
        ],
        red_flags: [],
        evidence: [
          {
            claim_id: "claim_001",
            source: "Reserve Bank of India Monetary Policy Handbook",
            text: "Inflation systematically erodes the real purchasing power of currency over time.",
            relevance_score: 0.98,
            url: "https://rbi.org.in"
          }
        ],
        explanation: "This content presents standard educational financial statements with no observable scam indicators.",
        safe_action: "Verify investment products against your personal risk tolerance and financial goals."
      };
    }

    if (contentLower.includes('sebi has approved')) {
      return {
        overall_risk: "HIGH",
        scam_score: 68,
        misinformation_score: 75,
        claims: [
          {
            id: "claim_001",
            text: "SEBI has approved our guaranteed-return investment scheme",
            type: "regulatory",
            status: "UNVERIFIED",
            reason: "SEBI does not approve guaranteed-return private investment schemes."
          }
        ],
        red_flags: [
          {
            type: "FAKE_AUTHORITY",
            severity: "HIGH",
            label: "Regulatory claim",
            description: "Claims SEBI endorsement for a guaranteed-return scheme."
          },
          {
            type: "GUARANTEED_RETURN",
            severity: "HIGH",
            label: "Guaranteed return",
            description: "Promises fixed returns which is prohibited for equity/market investments."
          }
        ],
        evidence: [
          {
            claim_id: "claim_001",
            source: "SEBI Official Caution Note",
            text: "Public notice: SEBI does not guarantee returns for any investment scheme or private entity.",
            relevance_score: 0.95,
            url: "https://www.sebi.gov.in"
          }
        ],
        explanation: "The message falsely cites SEBI regulatory approval to endorse a scheme promising guaranteed returns.",
        safe_action: "Verify the registration number directly on SEBI's official portal (sebi.gov.in) before investing."
      };
    }

    if (contentLower.includes('only 10 minutes') || contentLower.includes('crypto token')) {
      return {
        overall_risk: "HIGH",
        scam_score: 75,
        misinformation_score: 60,
        claims: [
          {
            id: "claim_001",
            text: "Double returns on crypto token launch",
            type: "financial_return",
            status: "UNSUPPORTED",
            reason: "Promising double returns on unverified token launches carries extreme loss risk."
          }
        ],
        red_flags: [
          {
            type: "URGENCY",
            severity: "MEDIUM",
            label: "Urgency",
            description: "Uses a 10-minute timer to rush financial transfers."
          },
          {
            type: "PAYMENT_REQUEST",
            severity: "HIGH",
            label: "Payment request",
            description: "Demands direct UPI transfer immediately."
          }
        ],
        evidence: [],
        explanation: "High urgency coupled with direct money transfer requests to private UPI accounts indicates an active scam.",
        safe_action: "Never transfer money or crypto based on high-pressure time limits."
      };
    }

    // Default Case 1 response
    return MOCK_RESPONSE_CASE_1;
  }

  // Real Backend API call (POST /analyze)
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server returned status ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (err) {
    console.error("API error:", err);
    throw new Error(err.message || 'Failed to connect to NiveshRakshak API server.');
  }
}
