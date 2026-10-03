"""
Unit tests for claims extraction.
"""
import pytest
from app.analysis.claims import extract_claims


def test_extract_claims_basic():
    text = "Invest ₹10,000 today and get guaranteed 30% returns in 7 days. SEBI approved."
    claims = extract_claims(text)
    
    assert len(claims) >= 2
    claim_texts = [c["text"].lower() for c in claims]
    
    assert any("30%" in ct or "guaranteed" in ct for ct in claim_texts)
    assert any("sebi" in ct for ct in claim_texts)
    
    # Verify structure
    for claim in claims:
        assert "id" in claim
        assert "text" in claim
        assert "type" in claim


def test_extract_claims_empty():
    assert extract_claims("") == []
    assert extract_claims("   ") == []


def test_extract_claims_educational():
    text = "Inflation reduces the purchasing power of money over time."
    claims = extract_claims(text)
    assert len(claims) >= 1
    assert "inflation" in claims[0]["text"].lower()
