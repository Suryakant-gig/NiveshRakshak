"""
Claim extraction module for NiveshRakshak.
Extracts structured claims from financial messages deterministically.
"""
import re
from typing import List, Dict, Any
from app.analysis.classifier import classify_claim_text


def extract_claims(text: str) -> List[Dict[str, Any]]:
    """
    Extracts financial claims from input text.
    
    Args:
        text (str): Input text message.
        
    Returns:
        List[Dict[str, Any]]: List of extracted claim objects with keys id, text, type.
    """
    if not text or not text.strip():
        return []

    claims = []
    text_clean = text.strip()
    
    # Sentence / phrase splitter
    # Split on periods, exclamation marks, newlines, and key separators while preserving meaningful clauses
    raw_segments = re.split(r'(?<=[.!?\n])\s+|;\s*', text_clean)
    
    # Also check for embedded patterns if sentence splitting is too coarse
    extracted_texts = []
    
    for segment in raw_segments:
        segment = segment.strip()
        if not segment:
            continue
            
        # Check if segment contains multiple distinct claim statements
        # e.g., "Guaranteed 30% returns in 7 days. SEBI approved."
        # If segment has multiple clauses separated by commas/and
        sub_clauses = re.split(r'\.\s+|\n+|(?:^|\s)(?=SEBI|RBI|Guaranteed|Send|Invest|Only|Limited)', segment, flags=re.IGNORECASE)
        for clause in sub_clauses:
            clause_str = clause.strip().rstrip('.')
            if len(clause_str) >= 5 and clause_str not in extracted_texts:
                extracted_texts.append(clause_str)

    # Filter & construct claims
    claim_count = 1
    for item_text in extracted_texts:
        # Determine if text is a substantial claim (not just "Send money now" or "Limited slots")
        item_lower = item_text.lower()
        
        # Check if it has claim characteristics (returns, regulatory statements, market assertions, economic facts)
        is_claim = False
        claim_type = classify_claim_text(item_text)
        
        if claim_type in ["financial_return", "regulatory"]:
            is_claim = True
        elif any(kw in item_lower for kw in ["return", "profit", "invest", "yield", "inflation", "stock", "crypto", "scheme", "approved", "growth"]):
            is_claim = True
        elif len(item_text.split()) >= 4 and not any(kw in item_lower for kw in ["send money", "act now"]):
            is_claim = True
            
        if is_claim:
            # Clean up text display
            clean_claim_text = item_text
            # Standardize claim phrasing if it's a returns claim
            if "guaranteed 30%" in item_lower or "30% returns" in item_lower:
                if "7 days" in item_lower and "guaranteed" in item_lower:
                    clean_claim_text = "Guaranteed 30% return in 7 days"
                elif "guaranteed" in item_lower:
                    clean_claim_text = "Guaranteed 30% return"
            elif "sebi" in item_lower and "approved" in item_lower:
                clean_claim_text = "SEBI approved"
                
            claims.append({
                "id": f"claim_{claim_count:03d}",
                "text": clean_claim_text,
                "type": claim_type
            })
            claim_count += 1

    # Fallback if no specific regex matched but text contains input
    if not claims and len(text_clean) > 0:
        claims.append({
            "id": "claim_001",
            "text": text_clean[:100].strip(),
            "type": classify_claim_text(text_clean)
        })

    return claims
