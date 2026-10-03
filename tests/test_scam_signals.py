"""
Unit tests for scam signal detection.
"""
import pytest
from app.analysis.scam_signals import detect_scam_signals


def test_detect_scam_signals_all():
    text = "Guaranteed 30% return in 7 days. Act now! Only 3 slots left. Send ₹10,000 to UPI now. SEBI approved scheme."
    signals = detect_scam_signals(text)
    
    types = [s["type"] for s in signals]
    assert "GUARANTEED_RETURN" in types
    assert "UNREALISTIC_RETURN" in types
    assert "URGENCY" in types
    assert "LIMITED_TIME" in types
    assert "PAYMENT_REQUEST" in types
    assert "FAKE_AUTHORITY" in types


def test_detect_scam_signals_legitimate():
    text = "Inflation reduces the purchasing power of money over time."
    signals = detect_scam_signals(text)
    assert len(signals) == 0


def test_detect_scam_signals_structure():
    text = "Guaranteed returns available."
    signals = detect_scam_signals(text)
    assert len(signals) >= 1
    s = signals[0]
    assert "type" in s
    assert "severity" in s
    assert "label" in s
    assert "description" in s


def test_fake_authority_variations():
    samples = [
        "SEBI has approved our guaranteed-return scheme.",
        "RBI approved high-yield plan.",
        "Officially approved by SEBI.",
        "Approved by the government."
    ]
    for text in samples:
        signals = detect_scam_signals(text)
        types = [s["type"] for s in signals]
        assert "FAKE_AUTHORITY" in types, f"Failed for text: {text}"


def test_authority_mention_without_approval():
    text = "SEBI released a circular regarding mutual funds."
    signals = detect_scam_signals(text)
    types = [s["type"] for s in signals]
    assert "FAKE_AUTHORITY" not in types


def test_guaranteed_and_unrealistic_return_detection():
    text = "Guaranteed 50% return"
    signals = detect_scam_signals(text)
    types = [s["type"] for s in signals]
    assert "GUARANTEED_RETURN" in types
    assert "UNREALISTIC_RETURN" in types
