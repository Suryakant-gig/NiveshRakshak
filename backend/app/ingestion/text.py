"""Text ingestion and normalization."""

import re
import unicodedata
from typing import Dict, Any


def detect_language(text: str) -> str:
    """Detect if text contains Devanagari script (Hindi) or defaults to English."""
    for char in text:
        if "\u0900" <= char <= "\u097F":
            return "hi"
    return "en"


def normalize_text(text: str) -> str:
    """
    Cleans and normalizes financial message text.
    - Preserves case-insensitive content
    - Normalizes unicode characters
    - Normalizes currency tokens (₹ / INR / Rs)
    - Strips noisy multiple spaces and emojis while keeping alphanumeric & core punctuation
    """
    if not text:
        return ""

    # Normalize unicode forms (NFKC)
    cleaned = unicodedata.normalize("NFKC", text)

    # Normalize currency representations: ₹ -> Rs.
    cleaned = re.sub(r"[₹]", "Rs. ", cleaned)

    # Collapse repeated whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def ingest_text(content: str) -> Dict[str, Any]:
    """
    Stage 2: Ingestion + Normalization
    Takes raw user text, normalizes it, and detects language.
    Returns:
        {
            "original_text": str,
            "normalized_text": str,
            "language": str
        }
    """
    original = content.strip() if content else ""
    normalized = normalize_text(original)
    language = detect_language(original)

    return {
        "original_text": original,
        "normalized_text": normalized,
        "language": language,
    }
