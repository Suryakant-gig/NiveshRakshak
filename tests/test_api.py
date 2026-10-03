

"""import pytest"""
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.ingestion.text import ingest_text, normalize_text, detect_language
from backend.app.llm.safety import apply_safety_guardrails
from backend.app.api.schemas import RiskLevel, VerificationStatus, ScamSignalType

client = TestClient(app)


# ---------------------------------------------------------------------------
# 1. Health & Meta Endpoints
# ---------------------------------------------------------------------------
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["contract_version"] == "1.0"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# 2. Ingestion & Normalization Tests (Stage 2)
# ---------------------------------------------------------------------------
def test_text_normalization():
    raw_text = "Invest   ₹10,000  today   and get guaranteed returns!  "
    normalized = normalize_text(raw_text)
    assert "₹" not in normalized
    assert "Rs." in normalized
    assert "   " not in normalized
    assert normalized.startswith("Invest Rs. 10,000")


def test_language_detection():
    hindi_text = "गारंटीड रिटर्न 30% प्रति माह"
    english_text = "Guaranteed return 30% per month"
    assert detect_language(hindi_text) == "hi"
    assert detect_language(english_text) == "en"


def test_ingest_text_output_contract():
    result = ingest_text("Invest ₹5000 now")
    assert "original_text" in result
    assert "normalized_text" in result
    assert "language" in result
    assert result["language"] == "en"


# ---------------------------------------------------------------------------
# 3. Safety Guardrails Tests (Stage 8)
# ---------------------------------------------------------------------------
def test_safety_guardrails_blocks_advice():
    prohibited_explanation = "You should buy the stock immediately because the market will rise."
    prohibited_safe_action = "Invest your money in this token now."

    clean_exp, clean_act = apply_safety_guardrails(prohibited_explanation, prohibited_safe_action)

    assert "buy the stock" not in clean_exp
    assert "market will rise" not in clean_exp
    assert clean_act != prohibited_safe_action
    assert "authoritative source" in clean_act


# ---------------------------------------------------------------------------
# 4. Error Handling & Validation
# ---------------------------------------------------------------------------
def test_empty_content_returns_400():
    response = client.post("/analyze", json={"content": ""})
    assert response.status_code == 400


def test_whitespace_content_returns_400():
    response = client.post("/analyze", json={"content": "   "})
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# 5. The 7 Frozen Demo Test Cases (Doc 1 & Doc 2)
# ---------------------------------------------------------------------------
def test_case_1_obvious_scam():
    """Case 1: Obvious scam -> HIGH risk, multiple red flags."""
    content = "Guaranteed 50% return in 7 days. Send ₹10,000 now."
    response = client.post("/analyze", json={"content": content})
    assert response.status_code == 200
    data = response.json()

    assert data["overall_risk"] == RiskLevel.HIGH
    assert data["scam_score"] >= 70
    assert len(data["red_flags"]) >= 2
    types = [f["type"] for f in data["red_flags"]]
    assert ScamSignalType.GUARANTEED_RETURN in types
    assert ScamSignalType.PAYMENT_REQUEST in types
    assert "safe_action" in data and len(data["safe_action"]) > 0


def test_case_2_fake_authority():
    """Case 2: Fake authority -> Regulatory claim flagged, claim UNVERIFIED."""
    content = "SEBI has approved our guaranteed-return scheme."
    response = client.post("/analyze", json={"content": content})
    assert response.status_code == 200
    data = response.json()

    types = [f["type"] for f in data["red_flags"]]
    assert ScamSignalType.FAKE_AUTHORITY in types

    # Must preserve UNVERIFIED != FALSE
    statuses = [c["status"] for c in data["claims"]]
    assert VerificationStatus.UNVERIFIED in statuses or VerificationStatus.UNSUPPORTED in statuses


def test_case_3_misinformation():
    """Case 3: Misinformation -> Claims UNSUPPORTED or UNVERIFIED."""
    content = "Guaranteed 30% returns every week on government bond investment."
    response = client.post("/analyze", json={"content": content})
    assert response.status_code == 200
    data = response.json()

    statuses = [c["status"] for c in data["claims"]]
    assert any(s in (VerificationStatus.UNSUPPORTED, VerificationStatus.UNVERIFIED) for s in statuses)


def test_case_4_legitimate_financial_education():
    """Case 4: Legitimate education -> LOWER risk, no false alarm."""
    content = "Index funds track a market benchmark and offer broad portfolio diversification with low fees."
    response = client.post("/analyze", json={"content": content})
    assert response.status_code == 200
    data = response.json()

    assert data["overall_risk"] == RiskLevel.LOW
    assert data["scam_score"] < 40


def test_case_5_ambiguous_content():
    """Case 5: Ambiguous claim -> UNVERIFIED shown, not labelled false."""
    content = "This new wealth strategy aims to outperform traditional fixed deposits over a 5 year horizon."
    response = client.post("/analyze", json={"content": content})
    assert response.status_code == 200
    data = response.json()

    # Rule: UNVERIFIED does not mean FALSE
    for claim in data["claims"]:
        assert claim["status"] != "FALSE"
    assert data["overall_risk"] in (RiskLevel.LOW, RiskLevel.MEDIUM)


def test_case_6_guaranteed_return_claim():
    """Case 6: Guaranteed-return claim -> GUARANTEED_RETURN flagged HIGH."""
    content = "Our automated trading bot delivers guaranteed 25% monthly return."
    response = client.post("/analyze", json={"content": content})
    assert response.status_code == 200
    data = response.json()

    types = [f["type"] for f in data["red_flags"]]
    assert ScamSignalType.GUARANTEED_RETURN in types
    severities = [f["severity"] for f in data["red_flags"] if f["type"] == ScamSignalType.GUARANTEED_RETURN]
    assert "HIGH" in severities


def test_case_7_urgency_based_message():
    """Case 7: Urgency-based message -> URGENCY flagged."""
    content = "Hurry! Act now immediately, only 3 spots remaining before this investment offer closes."
    response = client.post("/analyze", json={"content": content})
    assert response.status_code == 200
    data = response.json()

    types = [f["type"] for f in data["red_flags"]]
    assert ScamSignalType.URGENCY in types or ScamSignalType.LIMITED_TIME in types


def test_definition_of_done():
    """Section 11 Definition of Done:
    Input: 'Guaranteed 30% return in 7 days. SEBI approved. Send ₹10,000 today.'
    Output: HIGH RISK (score ~82), Red flags, Claims, Evidence, Explanation, Safe next step
    """
    content = "Guaranteed 30% return in 7 days. SEBI approved. Send ₹10,000 today."
    response = client.post("/analyze", json={"content": content})
    assert response.status_code == 200
    data = response.json()

    assert data["overall_risk"] == RiskLevel.HIGH
    assert data["scam_score"] >= 70
    assert len(data["red_flags"]) >= 3
    assert len(data["claims"]) >= 1
    assert "explanation" in data and len(data["explanation"]) > 0
    assert "safe_action" in data and len(data["safe_action"]) > 0

