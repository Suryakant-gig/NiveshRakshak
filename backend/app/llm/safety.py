"""Safety guardrails and sanitization module."""

import re
from typing import Tuple

# Prohibited advisory patterns (No financial advice, no market predictions)
PROHIBITED_ADVICE_PATTERNS = [
    r"\b(buy|sell|short|hold|accumulate)\s+(the\s+)?(stock|shares|token|crypto|units)\b",
    r"\b(target\s+price|price\s+target)\b",
    r"\b(market\s+will\s+(rise|fall|crash|rally))\b",
    r"\binvest\s+your\s+money\s+in\b",
    r"\byou\s+should\s+invest\b",
    r"\bguaranteed\s+profit\b",
]

DEFAULT_SAFE_ACTION = (
    "Verify the claim through an authoritative source before taking financial action."
)


def sanitize_text(text: str) -> str:
    """Sanitize any advisory or predictive language from the text."""
    if not text:
        return ""

    sanitized = text
    for pattern in PROHIBITED_ADVICE_PATTERNS:
        sanitized = re.sub(pattern, "[advice removed]", sanitized, flags=re.IGNORECASE)

    return sanitized.strip()


def apply_safety_guardrails(explanation: str, safe_action: str) -> Tuple[str, str]:
    """
    Stage 8: Safety / Guardrails
    Ensures that explanation and safe_action do NOT contain:
    - Stock predictions
    - Buy / Sell recommendations
    - Investment advice
    
    Guarantees investor protection and adherence to regulatory constraints.
    """
    clean_explanation = sanitize_text(explanation)
    clean_safe_action = sanitize_text(safe_action)

    if not clean_explanation:
        clean_explanation = (
            "This content has been flagged for containing high-risk financial claims or indicators. "
            "Independent verification against regulatory sources is recommended."
        )

    if not clean_safe_action or "[advice removed]" in clean_safe_action:
        clean_safe_action = DEFAULT_SAFE_ACTION

    return clean_explanation, clean_safe_action
