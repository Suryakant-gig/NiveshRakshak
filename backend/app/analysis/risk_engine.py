"""
Risk engine module for NiveshRakshak.
Calculates transparent scam and misinformation risk scores based on detected signals and claim statuses.
"""
from typing import List, Dict, Any


def calculate_risk(
    claims: List[Dict[str, Any]],
    scam_signals: List[Dict[str, Any]],
    verification_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calculates scam_score, misinformation_score, and overall_risk.
    
    Scoring methodology:
    - HIGH signal = 25 points
    - MEDIUM signal = 12 points
    - LOW signal = 5 points
    
    Misinformation scoring:
    - CONTRADICTED claim = 25 points
    - UNSUPPORTED claim = 20 points
    - UNVERIFIED claim = 10 points
    - SUPPORTED claim = 0 points
    
    Bands:
    - 0-39: LOW
    - 40-69: MEDIUM
    - 70-100: HIGH
    
    Args:
        claims: List of extracted claim dicts
        scam_signals: List of detected scam signal dicts
        verification_results: List of claim verification dicts (containing status)
        
    Returns:
        Dict with scam_score, misinformation_score, overall_risk.
    """
    # 1. Calculate Scam Score
    scam_points = 0
    for signal in scam_signals:
        severity = signal.get("severity", "LOW").upper()
        if severity == "HIGH":
            scam_points += 25
        elif severity == "MEDIUM":
            scam_points += 12
        elif severity == "LOW":
            scam_points += 5

    scam_score = min(100, scam_points)

    # 2. Calculate Misinformation Score
    misinfo_points = 0
    # Use verification_results if provided, otherwise fallback to claims status
    target_claims = verification_results if verification_results else claims
    
    if target_claims:
        for c in target_claims:
            status = c.get("status", "UNVERIFIED").upper()
            if status == "CONTRADICTED":
                misinfo_points += 25
            elif status == "UNSUPPORTED":
                misinfo_points += 20
            elif status == "UNVERIFIED":
                misinfo_points += 10
            elif status == "SUPPORTED":
                misinfo_points += 0
    else:
        misinfo_points = 0

    # If scam signals are present, misinformation confidence increases
    if scam_signals and misinfo_points > 0:
        misinfo_points += len(scam_signals) * 5

    misinformation_score = min(100, misinfo_points)

    # 3. Overall Risk Determination
    # Overall score is the composite max / weighted score
    composite_score = max(scam_score, misinformation_score)
    
    if composite_score >= 70:
        overall_risk = "HIGH"
    elif composite_score >= 40:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"

    return {
        "scam_score": scam_score,
        "misinformation_score": misinformation_score,
        "overall_risk": overall_risk
    }
