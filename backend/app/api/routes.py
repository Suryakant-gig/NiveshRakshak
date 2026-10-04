"""API routes for NiveshRakshak."""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException

from backend.app.api.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ClaimItem,
    RedFlagItem,
    EvidenceItem,
    VerificationStatus,
    RiskLevel,
    ScamSignalType,
)
from backend.app.ingestion.text import ingest_text
from backend.app.llm.client import generate_explanation_and_safe_action

logger = logging.getLogger(__name__)

router = APIRouter()

# ---------------------------------------------------------------------------
# Fallback / Mock implementations for Stage 1 (Nobody waits for another module)
# ---------------------------------------------------------------------------
def _default_extract_claims(text: str) -> List[Dict[str, Any]]:
    """Mock claim extractor """
    claims = []
    text_lower = text.lower()
    claim_idx = 1

    if "guaranteed" in text_lower or "%" in text_lower or "return" in text_lower:
        claims.append({
            "id": f"claim_{claim_idx:03d}",
            "text": "Guaranteed financial return",
            "type": "financial_return",
        })
        claim_idx += 1

    if "sebi" in text_lower or "approved" in text_lower or "registered" in text_lower or "rbi" in text_lower:
        claims.append({
            "id": f"claim_{claim_idx:03d}",
            "text": "Regulatory authority approval or registration",
            "type": "regulatory",
        })
        claim_idx += 1

    if not claims:
        claims.append({
            "id": f"claim_{claim_idx:03d}",
            "text": text[:80] + ("..." if len(text) > 80 else ""),
            "type": "general",
        })

    return claims


def _default_detect_scam_signals(text: str) -> List[Dict[str, Any]]:
    """Mock signal detector """
    import re

    signals = []
    text_lower = text.lower()

    if re.search(r"\b(guaranteed|guarantee|assured|100%\s*return)\b", text_lower):
        signals.append({
            "type": ScamSignalType.GUARANTEED_RETURN,
            "severity": "HIGH",
            "description": "Promises a guaranteed financial return.",
        })

    if re.search(r"\b(\d{2,}%\s*(return|profit|gain)|double your money|2x|3x|50%|30%|40%|100%)\b", text_lower):
        signals.append({
            "type": ScamSignalType.UNREALISTIC_RETURN,
            "severity": "HIGH",
            "description": "Return level or turnaround speed is implausibly high.",
        })

    if re.search(r"\b(hurry|urgent|fast|act now|immediately|instant)\b", text_lower):
        signals.append({
            "type": ScamSignalType.URGENCY,
            "severity": "MEDIUM",
            "description": "Psychological pressure to act immediately.",
        })

    if re.search(r"\b(limited slots?|limited time|few seats?|expires|only \d+ (slots?|spots?|seats?))\b", text_lower):
        signals.append({
            "type": ScamSignalType.LIMITED_TIME,
            "severity": "MEDIUM",
            "description": "Artificial scarcity or impending deadline.",
        })

    if re.search(r"\b(send|transfer|gpay|upi|paytm|deposit|invest)\b.*?(rs\.?|₹|money|cash|\d+|now|today)", text_lower):
        signals.append({
            "type": ScamSignalType.PAYMENT_REQUEST,
            "severity": "HIGH",
            "description": "Explicit solicitation to transfer funds.",
        })

    if re.search(r"\b(sebi|rbi|irda|govt|government)\b.*?(approv|register|certif|licens|endors)", text_lower):
        signals.append({
            "type": ScamSignalType.FAKE_AUTHORITY,
            "severity": "HIGH",
            "description": "Unverified claim of regulatory approval or official endorsement.",
        })

    return signals


def _default_retrieve_evidence(claim_text: str) -> List[Dict[str, Any]]:
    """Mock evidence retriever until P completes evidence engine."""
    claim_lower = claim_text.lower()
    if "sebi" in claim_lower or "regulat" in claim_lower:
        return [{
            "source": "SEBI Official Advisory (sebi.gov.in)",
            "text": "SEBI does not endorse or approve schemes promising guaranteed high returns.",
            "relevance_score": 0.94,
            "url": "https://www.sebi.gov.in/enforcement/unauthorized-schemes.html",
        }]
    if "return" in claim_lower or "guaranteed" in claim_lower:
        return [{
            "source": "RBI / SEBI Investor Awareness",
            "text": "Legitimate market-linked investments carry risk and cannot guarantee fixed high returns.",
            "relevance_score": 0.91,
            "url": "https://www.investor.sebi.gov.in",
        }]
    return []


def _default_verify_claim(claim_id: str, claim_text: str, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Mock claim verifier until P completes evidence engine."""
    claim_lower = claim_text.lower()
    if "guaranteed" in claim_lower:
        return {
            "claim_id": claim_id,
            "status": VerificationStatus.UNSUPPORTED,
            "reason": "Market-linked investments cannot promise guaranteed returns under SEBI regulations.",
            "evidence": evidence,
        }
    if "sebi" in claim_lower or "regulat" in claim_lower:
        return {
            "claim_id": claim_id,
            "status": VerificationStatus.UNVERIFIED,
            "reason": "No verifiable SEBI registration number or entity entry found.",
            "evidence": evidence,
        }
    return {
        "claim_id": claim_id,
        "status": VerificationStatus.UNVERIFIED,
        "reason": "No authoritative supporting evidence found.",
        "evidence": evidence,
    }


def _default_calculate_risk(
    claims: List[Dict[str, Any]],
    signals: List[Dict[str, Any]],
    verification_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Mock risk engine until """
    # Weight table from Architecture Contract v1.0
    weight_map = {"HIGH": 25, "MEDIUM": 12, "LOW": 5}
    scam_score = sum(weight_map.get(s.get("severity", "LOW"), 5) for s in signals)
    scam_score = min(scam_score, 100)

    # Misinformation calculation
    misinfo_score = 0
    for v in verification_results:
        status = v.get("status")
        if status in (VerificationStatus.CONTRADICTED, VerificationStatus.UNSUPPORTED):
            misinfo_score += 35
        elif status == VerificationStatus.UNVERIFIED:
            misinfo_score += 15
    misinfo_score = min(misinfo_score, 100)

    overall_score = max(scam_score, misinfo_score)
    if overall_score >= 70:
        overall_risk = RiskLevel.HIGH
    elif overall_score >= 40:
        overall_risk = RiskLevel.MEDIUM
    else:
        overall_risk = RiskLevel.LOW

    return {
        "scam_score": scam_score,
        "misinformation_score": misinfo_score,
        "overall_risk": overall_risk,
    }


# ---------------------------------------------------------------------------
# Dynamic import wrappers (Calling peer modules if implemented)
# ---------------------------------------------------------------------------
def run_claim_extraction(text: str) -> List[Dict[str, Any]]:
    try:
        from backend.app.analysis.claims import extract_claims
        res = extract_claims(text)
        if res:
            return res
    except Exception as e:
        logger.debug("Falling back to internal claim extraction: %s", e)
    return _default_extract_claims(text)


def run_scam_signals(text: str) -> List[Dict[str, Any]]:
    try:
        from backend.app.analysis.scam_signals import detect_scam_signals
        res = detect_scam_signals(text)
        if res:
            return res
    except Exception as e:
        logger.debug("Falling back to internal scam signal detection: %s", e)
    return _default_detect_scam_signals(text)


def run_evidence_and_verification(claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    verification_results = []
    for claim in claims:
        c_id = claim.get("id", "claim_001")
        c_text = claim.get("text", "")
        evidence_list = []
        try:
            from backend.app.retrieval.hybrid import retrieve_evidence
            evidence_list = retrieve_evidence(c_text)
        except Exception:
            evidence_list = _default_retrieve_evidence(c_text)

        v_res = None
        try:
            from backend.app.evidence.verifier import verify_claim
            v_res = verify_claim(c_text, evidence_list)
            if v_res and "claim_id" not in v_res:
                v_res["claim_id"] = c_id
        except Exception:
            v_res = _default_verify_claim(c_id, c_text, evidence_list)

        if not v_res:
            v_res = _default_verify_claim(c_id, c_text, evidence_list)

        verification_results.append(v_res)
    return verification_results

def run_risk_engine(
    claims: List[Dict[str, Any]],
    signals: List[Dict[str, Any]],
    verification_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    try:
        from backend.app.analysis.risk_engine import calculate_risk
        res = calculate_risk(claims, signals, verification_results)
        if res and "overall_risk" in res:
            return res
    except Exception as e:
        logger.debug("Falling back to internal risk calculation: %s", e)
    return _default_calculate_risk(claims, signals, verification_results)


# ---------------------------------------------------------------------------
# Core POST /analyze Endpoint
# ---------------------------------------------------------------------------
@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Main analysis pipeline conforming to FROZEN v1.0 contract.
    Flow:
    1. Ingestion + Normalization
    2. Claim Extraction (3a) & Scam Signal Detection (3b)
    3. Evidence Retrieval (4, 5) & Claim Verification (6)
    4. Risk Engine (7)
    5. Safety / Guardrails (8) & Explanation Generation
    6. Flatten Evidence & Build Final Report (9)
    """
    if not request.content or not request.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty.")

    # Step 2: Ingestion & Normalization 
    ingested = ingest_text(request.content)
    normalized_text = ingested["normalized_text"]
    original_text = ingested["original_text"]

    # Step 3: Analysis layer 
    claims_raw = run_claim_extraction(normalized_text)
    signals_raw = run_scam_signals(normalized_text)

    # Step 4-6: Evidence retrieval and verification (P)
    verification_results = run_evidence_and_verification(claims_raw)

    # Map verification results onto claims
    v_map = {v.get("claim_id"): v for v in verification_results}
    claims_processed = []
    for c in claims_raw:
        c_id = c.get("id")
        v_info = v_map.get(c_id, {})
        claims_processed.append(
            ClaimItem(
                id=c_id,
                text=c.get("text", ""),
                type=c.get("type"),
                status=v_info.get("status", VerificationStatus.UNVERIFIED),
                reason=v_info.get("reason"),
            )
        )

    # Step 7: Risk Engine 
    risk_output = run_risk_engine(
        claims_raw, signals_raw, verification_results
    )

    # Flatten evidence list from P's verification output (Section 11 Contract)
    all_evidence: List[EvidenceItem] = []
    for v in verification_results:
        c_id = v.get("claim_id", "")
        ev_items = v.get("evidence", [])
        for ev in ev_items:
            all_evidence.append(
                EvidenceItem(
                    claim_id=c_id,
                    source=ev.get("source", "Official Source"),
                    text=ev.get("text", ""),
                    relevance_score=float(ev.get("relevance_score", 0.0)),
                    url=ev.get("url"),
                )
            )

    # Step 8 & 9: Safety Guardrails + LLM Explanation / Safe Action 
    explanation, safe_action = generate_explanation_and_safe_action(
        original_text=original_text,
        claims=[c.model_dump() for c in claims_processed],
        signals=signals_raw,
        evidence=[e.model_dump() for e in all_evidence],
        risk_assessment=risk_output,
    )

    red_flags = [
        RedFlagItem(
            type=s.get("type", "UNKNOWN"),
            severity=s.get("severity", "MEDIUM"),
            description=s.get("description", s.get("type", "")),
        )
        for s in signals_raw
    ]

    return AnalyzeResponse(
        overall_risk=risk_output.get("overall_risk", RiskLevel.MEDIUM),
        scam_score=int(risk_output.get("scam_score", 0)),
        misinformation_score=int(risk_output.get("misinformation_score", 0)),
        claims=claims_processed,
        red_flags=red_flags,
        evidence=all_evidence,
        explanation=explanation,
        safe_action=safe_action,
    )
