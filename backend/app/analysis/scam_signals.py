"""
Scam signal detection module for NiveshRakshak.
Detects observable financial scam indicators deterministically.
"""
import re
from typing import List, Dict, Any


def detect_scam_signals(text: str) -> List[Dict[str, Any]]:
    """
    Detects observable scam signals in text.
    
    Required signal types:
    - GUARANTEED_RETURN
    - UNREALISTIC_RETURN
    - URGENCY
    - LIMITED_TIME
    - PAYMENT_REQUEST
    - FAKE_AUTHORITY
    
    Args:
        text (str): Input text message.
        
    Returns:
        List[Dict[str, Any]]: Detected scam signals with type, severity, label, description.
    """
    if not text or not text.strip():
        return []

    signals = []
    text_lower = text.lower()
    
    # 1. GUARANTEED_RETURN (HIGH)
    if re.search(r'guarant(?:ee|eed)|100%\s*risk[- ]free|sure\s*return|zero\s*risk|fixed\s*return', text_lower):
        signals.append({
            "type": "GUARANTEED_RETURN",
            "severity": "HIGH",
            "label": "Guaranteed Return",
            "description": "Promises a guaranteed return, which violates market principles and regulatory standards."
        })

    # 2. UNREALISTIC_RETURN (HIGH)
    if re.search(r'\d+%\s*(?:returns?|profit|yield|in\s*\d+\s*(?:days?|weeks?|hours?)|daily|weekly|monthly)|double\s*(?:your\s*)?money|30%\s*returns?|50%\s*return', text_lower):
        signals.append({
            "type": "UNREALISTIC_RETURN",
            "severity": "HIGH",
            "label": "Unrealistic Return",
            "description": "Promises abnormally high or rapid returns that are unrealistic for regulated investments."
        })

    # 3. URGENCY (MEDIUM)
    if re.search(r'act\s+now|hurry|send\s+money\s+now|now\b|expires?\s+soon|last\s+chance|only\s+\d+\s+minutes?\s+left|immediately', text_lower):
        signals.append({
            "type": "URGENCY",
            "severity": "MEDIUM",
            "label": "Urgency",
            "description": "Pressures the user to act immediately before verifying details."
        })

    # 4. LIMITED_TIME / LIMITED_SLOTS (MEDIUM)
    if re.search(r'limited\s+slots?|only\s+\d+\s+slots?|today\s+only|exclusive\s+slot|slots?\s+available', text_lower):
        signals.append({
            "type": "LIMITED_TIME",
            "severity": "MEDIUM",
            "label": "Limited Slots",
            "description": "Creates artificial scarcity to rush the user into sending funds."
        })

    # 5. PAYMENT_REQUEST (HIGH)
    if re.search(r'send\s+money|transfer|deposit|pay\s+(?:to|now|money)|(?:send|pay|transfer|deposit)\s*(?:rs\.?|₹|\$|inr)?\s*\d+|upi|gpay|phonepe', text_lower):
        signals.append({
            "type": "PAYMENT_REQUEST",
            "severity": "HIGH",
            "label": "Payment Request",
            "description": "Requests direct money transfer or payment upfront."
        })

    # 6. FAKE_AUTHORITY / REGULATORY_CLAIM (HIGH)
    if re.search(
        r'\b(?:sebi|rbi|irdai|sec|pfrda|govt|government|financial\s+authority)\s+(?:has\s+|is\s+|was\s+|officially\s+)?(?:approved|registered|certified|authorized|verified|licensed|endorsed|backed)\b'
        r'|\b(?:officially\s+)?(?:approved|registered|certified|authorized|verified|licensed|endorsed|backed)\s+by\s+(?:the\s+)?(?:sebi|rbi|irdai|sec|pfrda|govt|government|financial\s+authority)\b'
        r'|\bgovernment\s+(?:has\s+|is\s+|was\s+)?(?:backed|approved|registered|certified|authorized|guaranteed)\b',
        text_lower
    ):
        signals.append({
            "type": "FAKE_AUTHORITY",
            "severity": "HIGH",
            "label": "Regulatory Claim",
            "description": "Claims regulatory approval (SEBI/RBI) to artificially build false credibility."
        })

    return signals
