/**
 * Centralized mock response dataset and demo cases for NiveshRakshak.
 * Strictly conforms to Section 12 API Contract.
 */

export const MOCK_RESPONSE_CASE_1 = {
  overall_risk: "HIGH",
  scam_score: 82,
  misinformation_score: 71,
  claims: [
    {
      id: "claim_001",
      text: "Guaranteed 30% returns in 7 days",
      type: "financial_return",
      status: "UNSUPPORTED",
      reason: "No regulated market product can legally guarantee 30% returns in 7 days."
    },
    {
      id: "claim_002",
      text: "SEBI approved scheme",
      type: "regulatory",
      status: "UNVERIFIED",
      reason: "Claimed regulatory registration could not be verified in the SEBI official registry."
    }
  ],
  red_flags: [
    {
      type: "GUARANTEED_RETURN",
      severity: "HIGH",
      label: "Guaranteed return",
      description: "Promises a guaranteed return on investment, violating market regulations."
    },
    {
      type: "UNREALISTIC_RETURN",
      severity: "HIGH",
      label: "Unrealistic return",
      description: "Promises 30% returns in 7 days, which is inconsistent with market realities."
    },
    {
      type: "URGENCY",
      severity: "MEDIUM",
      label: "Urgency",
      description: "Pressures the user to act immediately before performing due diligence."
    },
    {
      type: "PAYMENT_REQUEST",
      severity: "HIGH",
      label: "Payment request",
      description: "Requests immediate money transfer via direct payment."
    },
    {
      type: "FAKE_AUTHORITY",
      severity: "HIGH",
      label: "Regulatory claim",
      description: "Uses SEBI name to build false trust for an unauthorized scheme."
    }
  ],
  evidence: [
    {
      claim_id: "claim_001",
      source: "SEBI Investor Advisory Bulletin",
      text: "SEBI explicitly warns investors against schemes offering guaranteed or fixed returns on market investments. Registered intermediaries are prohibited from guaranteeing returns.",
      relevance_score: 0.94,
      url: "https://www.sebi.gov.in"
    },
    {
      claim_id: "claim_002",
      source: "RBI Sachet Fraud Portal",
      text: "Unauthorized entities frequently misrepresent approval from SEBI/RBI to solicit public funds.",
      relevance_score: 0.88,
      url: "https://sachet.rbi.org.in"
    }
  ],
  explanation: "This content contains multiple severe risk signals including a guaranteed-return promise, unrealistic 7-day timeline, urgency pressure, and unverified SEBI endorsement.",
  safe_action: "Verify the claim through an authoritative source (e.g., official SEBI/RBI portal) before taking financial action."
};

export const DEMO_PRESETS = [
  {
    id: "case-1",
    title: "Case 1: Obvious Scam",
    badge: "High Risk",
    badgeColor: "red",
    text: "Invest ₹10,000 today and get guaranteed 30% returns in 7 days. SEBI approved. Limited slots available. Send money now."
  },
  {
    id: "case-2",
    title: "Case 2: Fake Authority",
    badge: "Regulatory Claim",
    badgeColor: "amber",
    text: "SEBI has approved our guaranteed-return investment scheme. Register before the portal closes."
  },
  {
    id: "case-3",
    title: "Case 3: Legitimate Education",
    badge: "Low Risk",
    badgeColor: "emerald",
    text: "Inflation reduces the purchasing power of money over time. Diversifying asset allocation helps manage long-term portfolio risk."
  },
  {
    id: "case-4",
    title: "Case 4: Ambiguous Claim",
    badge: "Unverified",
    badgeColor: "cyan",
    text: "Invest in this exclusive opportunity for excellent returns and high capital growth over the next quarter."
  },
  {
    id: "case-5",
    title: "Case 5: High Urgency",
    badge: "Urgency Signal",
    badgeColor: "purple",
    text: "Only 10 minutes left to claim double returns on crypto token launch. Send money to UPI address now."
  }
];
