"""
Unit tests for risk engine scoring.
"""
import pytest
from app.analysis.risk_engine import calculate_risk


def test_calculate_risk_high():
    claims = [
        {"id": "claim_001", "text": "Guaranteed 30% return", "status": "UNSUPPORTED"},
        {"id": "claim_002", "text": "SEBI approved", "status": "UNVERIFIED"}
    ]
    signals = [
        {"type": "GUARANTEED_RETURN", "severity": "HIGH"},
        {"type": "UNREALISTIC_RETURN", "severity": "HIGH"},
        {"type": "URGENCY", "severity": "MEDIUM"},
        {"type": "PAYMENT_REQUEST", "severity": "HIGH"}
    ]
    
    result = calculate_risk(claims, signals, claims)
    assert result["scam_score"] >= 70
    assert result["overall_risk"] == "HIGH"


def test_calculate_risk_low():
    claims = [
        {"id": "claim_001", "text": "Inflation lowers purchasing power", "status": "SUPPORTED"}
    ]
    signals = []
    
    result = calculate_risk(claims, signals, claims)
    assert result["scam_score"] == 0
    assert result["misinformation_score"] == 0
    assert result["overall_risk"] == "LOW"


def test_calculate_risk_medium():
    claims = [
        {"id": "claim_001", "text": "Invest in this scheme", "status": "UNVERIFIED"}
    ]
    signals = [
        {"type": "URGENCY", "severity": "MEDIUM"},
        {"type": "LIMITED_TIME", "severity": "MEDIUM"},
        {"type": "PAYMENT_REQUEST", "severity": "MEDIUM"}
    ]
    
    result = calculate_risk(claims, signals, claims)
    assert 20 <= result["scam_score"] <= 69
    assert result["overall_risk"] in ["LOW", "MEDIUM"]
