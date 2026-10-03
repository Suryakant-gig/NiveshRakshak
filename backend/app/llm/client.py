"""LLM client for explanation and safe_action generation with robust fallback."""

import json
import logging
from typing import List, Dict, Any, Tuple
from backend.app.config import settings
from backend.app.llm.prompts import (
    EXPLANATION_SYSTEM_PROMPT,
    EXPLANATION_USER_PROMPT_TEMPLATE,
)
from backend.app.llm.safety import apply_safety_guardrails

logger = logging.getLogger(__name__)


def generate_fallback_explanation(
    original_text: str,
    claims: List[Dict[str, Any]],
    signals: List[Dict[str, Any]],
    risk_assessment: Dict[str, Any],
) -> Tuple[str, str]:
    """
    Deterministic rule-based explanation and safe_action generator.
    Guarantees reliable operation without external API dependencies.
    """
    overall_risk = risk_assessment.get("overall_risk", "MEDIUM")
    scam_score = risk_assessment.get("scam_score", 0)

    # Summarize signals
    signal_descriptions = [
        s.get("description") or s.get("type", "").replace("_", " ").title()
        for s in signals
    ]
    unverified_claims = [c for c in claims if c.get("status") == "UNVERIFIED"]
    unsupported_claims = [c for c in claims if c.get("status") in ("UNSUPPORTED", "CONTRADICTED")]

    parts = []
    if signal_descriptions:
        parts.append(
            f"The content contains red flag indicators: {', '.join(signal_descriptions)}."
        )

    if unsupported_claims:
        claims_str = ", ".join(f'"{c.get("text")}"' for c in unsupported_claims)
        parts.append(f"Claim(s) {claims_str} are unsupported or contradicted by official evidence.")
    elif unverified_claims:
        claims_str = ", ".join(f'"{c.get("text")}"' for c in unverified_claims)
        parts.append(
            f"Claim(s) {claims_str} remain unverified as no authoritative evidence was found. "
            "(Note: unverified does not necessarily mean false, but warrants caution)."
        )

    if not parts:
        if overall_risk == "LOW":
            parts.append(
                "The content presents standard financial or educational information with no significant scam red flags detected."
            )
        else:
            parts.append(
                f"The content has an assessed risk score of {scam_score}/100 based on automated heuristics."
            )

    explanation = " ".join(parts)

    if overall_risk == "HIGH":
        safe_action = (
            "Do not send money or share personal financial details. "
            "Verify registration numbers directly on SEBI's official portal (sebi.gov.in) before acting."
        )
    elif overall_risk == "MEDIUM":
        safe_action = (
            "Verify the claim through an authoritative source before taking financial action."
        )
    else:
        safe_action = (
            "Always independently verify investment opportunities and ensure they align with your financial goals."
        )

    return explanation, safe_action


def generate_explanation_and_safe_action(
    original_text: str,
    claims: List[Dict[str, Any]],
    signals: List[Dict[str, Any]],
    evidence: List[Dict[str, Any]],
    risk_assessment: Dict[str, Any],
) -> Tuple[str, str]:
    """
    Generates explanation and safe_action using LLM (if configured) or deterministic fallback.
    Results are strictly passed through safety guardrails.
    """
    explanation = ""
    safe_action = ""

    # Attempt LLM call if GROQ API key is present
    if settings.GROQ_API_KEY:
        try:
            from openai import OpenAI

            client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=settings.GROQ_API_KEY,
            )

            signals_summary = "\n".join(
                [f"- {s.get('type')}: {s.get('description', '')} (Severity: {s.get('severity')})" for s in signals]
            ) or "None detected"

            claims_summary = "\n".join(
                [f"- \"{c.get('text')}\" [Status: {c.get('status', 'UNVERIFIED')}]" for c in claims]
            ) or "No distinct financial claims extracted"

            evidence_summary = "\n".join(
                [f"- Source: {e.get('source')}, Relevance: {e.get('relevance_score')}: {e.get('text')}" for e in evidence]
            ) or "No external evidence retrieved"

            user_prompt = EXPLANATION_USER_PROMPT_TEMPLATE.format(
                original_text=original_text,
                overall_risk=risk_assessment.get("overall_risk", "MEDIUM"),
                scam_score=risk_assessment.get("scam_score", 0),
                misinformation_score=risk_assessment.get("misinformation_score", 0),
                signals_summary=signals_summary,
                claims_summary=claims_summary,
                evidence_summary=evidence_summary,
            )

            response = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": EXPLANATION_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
            )

            raw_content = response.choices[0].message.content
            parsed = json.loads(raw_content)
            explanation = parsed.get("explanation", "")
            safe_action = parsed.get("safe_action", "")
        except Exception as e:
            logger.warning("LLM generation failed, falling back to deterministic engine: %s", e)

    # Use fallback if explanation is not generated
    if not explanation or not safe_action:
        explanation, safe_action = generate_fallback_explanation(
            original_text, claims, signals, risk_assessment
        )

    # Stage 8: Safety / Guardrails
    sanitized_explanation, sanitized_safe_action = apply_safety_guardrails(
        explanation, safe_action
    )

    return sanitized_explanation, sanitized_safe_action
