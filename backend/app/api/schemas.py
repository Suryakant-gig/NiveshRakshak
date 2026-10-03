"""Pydantic request/response schemas and domain models."""

from typing import List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Controlled Vocabulary Constants
# ---------------------------------------------------------------------------
class RiskLevel:
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class VerificationStatus:
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNVERIFIED = "UNVERIFIED"


class ScamSignalType:
    GUARANTEED_RETURN = "GUARANTEED_RETURN"
    UNREALISTIC_RETURN = "UNREALISTIC_RETURN"
    URGENCY = "URGENCY"
    LIMITED_TIME = "LIMITED_TIME"
    PAYMENT_REQUEST = "PAYMENT_REQUEST"
    FAKE_AUTHORITY = "FAKE_AUTHORITY"


# ---------------------------------------------------------------------------
# Ingestion Models
# ---------------------------------------------------------------------------
class NormalizedContent(BaseModel):
    original_text: str
    normalized_text: str
    language: str = "en"


# ---------------------------------------------------------------------------
# API Shared Contracts (FROZEN v1.0)
# ---------------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    content: str = Field(..., description="Raw pasted financial text to analyze.")


class ClaimItem(BaseModel):
    id: str
    text: str
    status: str = Field(
        default=VerificationStatus.UNVERIFIED,
        description="SUPPORTED, CONTRADICTED, UNSUPPORTED, or UNVERIFIED",
    )
    type: Optional[str] = None
    reason: Optional[str] = None


class RedFlagItem(BaseModel):
    type: str
    severity: str = Field(..., description="LOW, MEDIUM, or HIGH")
    description: str


class EvidenceItem(BaseModel):
    claim_id: str
    source: str
    text: str
    relevance_score: float
    url: Optional[str] = None


class AnalyzeResponse(BaseModel):
    overall_risk: str = Field(..., description="LOW, MEDIUM, or HIGH")
    scam_score: int = Field(..., ge=0, le=100)
    misinformation_score: int = Field(..., ge=0, le=100)
    claims: List[ClaimItem] = Field(default_factory=list)
    red_flags: List[RedFlagItem] = Field(default_factory=list)
    evidence: List[EvidenceItem] = Field(default_factory=list)
    explanation: str
    safe_action: str
