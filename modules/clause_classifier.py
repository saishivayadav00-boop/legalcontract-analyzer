import re
from typing import List, Dict

CLAUSE_KEYWORDS = {
    "Termination": [
        "termination", "terminate", "cancellation", "cancel", "expiration",
        "expire", "cure period", "notice of termination", "term of this agreement",
        "right to terminate", "terminated"
    ],
    "Confidentiality": [
        "confidential", "confidentiality", "nondisclosure", "non-disclosure",
        "proprietary information", "trade secret", "secrecy", "shall not disclose",
        "receiving party", "disclosing party"
    ],
    "Payment": [
        "payment", "fee", "fees", "invoice", "compensation", "billing",
        "remittance", "consideration", "due date", "price", "reimbursement",
        "interest rate", "payable"
    ],
    "Liability": [
        "limitation of liability", "liable", "liability", "consequential damages",
        "indirect damages", "maximum liability", "disclaimer of liability",
        "punitive damages", "incidental damages"
    ],
    "Indemnification": [
        "indemnify", "indemnification", "indemnity", "hold harmless",
        "defend and hold", "indemnified party", "indemnifying party"
    ],
    "Governing Law": [
        "governing law", "choice of law", "jurisdiction", "venue", "governed by",
        "laws of the state", "exclusive jurisdiction", "courts of", "governed by and construed"
    ],
    "Non-Compete": [
        "non-compete", "non compete", "non-solicitation", "non solicitation",
        "competing business", "solicit employees", "solicit customers",
        "covenant not to compete", "restraint of trade"
    ]
}

def classify_clause(clause_text: str) -> str:
    """
    Classifies a single clause text using keyword matching into one of:
    - Termination
    - Confidentiality
    - Payment
    - Liability
    - Indemnification
    - Governing Law
    - Non-Compete
    - Other / General (if no match)
    """
    if not clause_text or not clause_text.strip():
        return "Other / General"
        
    text_lower = clause_text.lower()
    scores = {}
    
    for category, keywords in CLAUSE_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in text_lower:
                # Weight multi-word phrases higher than single words
                score += len(kw.split())
        if score > 0:
            scores[category] = score
            
    if not scores:
        return "Other / General"
        
    # Return the category with highest match score
    return max(scores, key=scores.get)

def classify_clauses(clauses: List[str]) -> List[Dict[str, str]]:
    """
    Classifies a list of clauses into structured dictionaries.
    
    Returns:
        List[Dict[str, str]]: List of dicts containing 'Clause' and 'Clause Type'.
    """
    classified_results = []
    for clause in clauses:
        clause_type = classify_clause(clause)
        classified_results.append({
            "Clause": clause,
            "Clause Type": clause_type
        })
    return classified_results
