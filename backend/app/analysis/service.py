"""
Analysis service for NiveshRakshak.
Orchestrates claim extraction, scam signal detection, risk engine scoring,
and formats the strict API contract output.
"""
from typing import Dict, Any, List
from app.analysis.claims import extract_claims
from app.analysis.scam_signals import detect_scam_signals
from app.analysis.risk_engine import calculate_risk
from app.analysis.classifier import determine_initial_claim_status


def analyze_financial_text(text: str) -> Dict[str, Any]:
    """
    Analyzes input text and produces the full structured NiveshRakshak API response.
    
    Args:
        text (str): Input text message to analyze.
        
    Returns:
        Dict[str, Any]: Conforming to Section 12 API contract.
    """
    if not text or not text.strip():
        return {
            "overall_risk": "LOW",
            "scam_score": 0,
            "misinformation_score": 0,
            "claims": [],
            "red_flags": [],
            "evidence": [],
            "explanation": "No text content was provided for analysis.",
            "safe_action": "Verify all financial claims through official regulatory registries before investing."
        }

    # 1. Extract claims
    raw_claims = extract_claims(text)

    # 2. Detect scam signals
    scam_signals = detect_scam_signals(text)
    has_high_signals = any(s.get("severity") == "HIGH" for s in scam_signals)

    # 3. Enrich claims with verification status and reasons
    enriched_claims = []
    evidence_list = []
    
    for claim in raw_claims:
        c_type = claim.get("type", "market_claim")
        c_text = claim.get("text", "")
        
        status, reason = determine_initial_claim_status(c_type, c_text, has_high_signals)
        
        enriched_claim = {
            "id": claim.get("id"),
            "text": c_text,
            "type": c_type,
            "status": status,
            "reason": reason
        }
        enriched_claims.append(enriched_claim)
        
        # Add sample regulatory / official evidence placeholder if relevant (e.g. SEBI circulars)
        if c_type == "regulatory" or "sebi" in c_text.lower():
            evidence_list.append({
                "claim_id": claim.get("id"),
                "source": "SEBI Investor Advisory & Public Circulars",
                "text": "SEBI explicitly mandates that no registered entity can guarantee fixed returns on equity or market securities.",
                "relevance_score": 0.94,
                "url": "https://www.sebi.gov.in"
            })
        elif "guaranteed" in c_text.lower() or "30%" in c_text.lower():
            evidence_list.append({
                "claim_id": claim.get("id"),
                "source": "RBI / SEBI High-Yield Investment Fraud Warnings",
                "text": "High fixed return promises above prevailing benchmark rates without principal risk represent classic high-risk indicators.",
                "relevance_score": 0.89,
                "url": "https://sachet.rbi.org.in"
            })

    # 4. Calculate Risk
    risk_res = calculate_risk(enriched_claims, scam_signals, enriched_claims)
    
    # 5. Format Red Flags (matching scam_signals format)
    red_flags = []
    for s in scam_signals:
        red_flags.append({
            "type": s.get("type"),
            "severity": s.get("severity"),
            "label": s.get("label"),
            "description": s.get("description")
        })

    # 6. Build Explanation
    if scam_signals:
        flag_labels = ", ".join([s.get("label", "").lower() for s in scam_signals])
        explanation = (
            f"This content was flagged with an overall risk score of {max(risk_res['scam_score'], risk_res['misinformation_score'])}/100. "
            f"It contains key observable risk indicators including: {flag_labels}. "
            f"Claims of guaranteed returns or unverified regulatory backing require immediate caution."
        )
    elif enriched_claims:
        explanation = (
            "The text contains financial claims that could not be independently verified. "
            "No aggressive scam signals were detected, but caution is advised when evaluating unverified assertions."
        )
    else:
        explanation = "The content presents standard financial statements with low observable scam risk."

    # 7. Safe Action
    safe_action = "Verify the claim through an authoritative source (e.g. official SEBI/RBI portal) before taking financial action."

    # Construct final API response
    return {
        "overall_risk": risk_res["overall_risk"],
        "scam_score": risk_res["scam_score"],
        "misinformation_score": risk_res["misinformation_score"],
        "claims": enriched_claims,
        "red_flags": red_flags,
        "evidence": evidence_list,
        "explanation": explanation,
        "safe_action": safe_action
    }
