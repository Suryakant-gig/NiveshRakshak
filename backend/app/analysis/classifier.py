"""
Classifier module for identifying claim categories, patterns, and verification status defaults.
Deterministic and lightweight regex/NLP based classification.
"""
import re
from typing import List, Dict, Any

# Pattern definitions for claim classification
RETURN_PATTERNS = [
    r'guaranteed\s+(\d+%\s*returns?|\d+%\s*profit|\d+%\s*in\s*\d+\s*(?:days?|weeks?|months?))',
    r'(\d+%\s*returns?|\d+%\s*profit|\d+%\s*in\s*\d+\s*(?:days?|weeks?|months?))',
    r'(get|earn|make|double)\s+(?:guaranteed\s+)?(?:₹|\$)?\d+',
    r'fixed\s+(?:return|profit|yield)\s+of\s+\d+%',
    r'doubl(?:e|ing)\s+your\s+money',
    r'risk[- ]free\s+(?:investment|return|profit)',
]

REGULATORY_PATTERNS = [
    r'(?:sebi|rbi|irdai|sec|pfrda|financial\s+authority)\s+(?:has\s+|is\s+|was\s+|officially\s+)?(?:approved|registered|certified|authorized|verified|licensed|endorsed|backed)',
    r'(?:officially\s+)?(?:approved|registered|certified|authorized|verified|licensed|endorsed|backed)\s+by\s+(?:the\s+)?(?:sebi|rbi|irdai|sec|pfrda|govt|government|financial\s+authority)',
    r'government\s+(?:has\s+|is\s+|was\s+)?(?:backed|approved|registered|certified|authorized|guaranteed)',
]

URGENCY_PATTERNS = [
    r'limited\s+slots?\s*(?:available|left)?',
    r'only\s+\d+\s+slots?\s*(?:left|remaining)',
    r'(?:act|send|invest)\s+now',
    r'(?:offer|valid)\s+(?:for|ends?\s+in)\s+\d+\s*(?:mins?|minutes?|hours?|days?)',
    r'last\s+chance\s+to\s+invest',
]

PAYMENT_PATTERNS = [
    r'(?:send|transfer|deposit|pay)\s*(?:rs\.?|₹|\$|inr)?\s*\d+',
    r'(?:upi|gpay|phonepe|bank\s+transfer)\s+(?:payment|transfer|deposit)',
]


def classify_claim_text(claim_text: str) -> str:
    """
    Categorizes a claim text into a standardized type:
    - financial_return
    - regulatory
    - urgency_offer
    - payment_request
    - market_claim
    """
    text_lower = claim_text.lower()
    
    for pat in RETURN_PATTERNS:
        if re.search(pat, text_lower):
            return "financial_return"
            
    for pat in REGULATORY_PATTERNS:
        if re.search(pat, text_lower):
            return "regulatory"
            
    for pat in URGENCY_PATTERNS:
        if re.search(pat, text_lower):
            return "urgency_offer"
            
    for pat in PAYMENT_PATTERNS:
        if re.search(pat, text_lower):
            return "payment_request"
            
    return "market_claim"


def determine_initial_claim_status(claim_type: str, claim_text: str, has_high_scam_signals: bool) -> tuple[str, str]:
    """
    Determines initial verification status and reason for a claim in absence of external RAG proof.
    Statuses: SUPPORTED, CONTRADICTED, UNSUPPORTED, UNVERIFIED.
    """
    text_lower = claim_text.lower()
    
    if claim_type == "financial_return":
        if "guaranteed" in text_lower or has_high_scam_signals:
            return "UNSUPPORTED", "No regulatory or authoritative evidence supports guaranteed high market returns."
        return "UNVERIFIED", "Requires verification against official fund prospectuses or market data."
        
    if claim_type == "regulatory":
        return "UNVERIFIED", "Claimed regulatory approval is not verified in official SEBI/RBI public registries."
        
    if "inflation" in text_lower or "purchasing power" in text_lower:
        return "SUPPORTED", "Established economic fact documented by central banks and standard economic literature."
        
    return "UNVERIFIED", "Verification requires checking against official financial sources."
