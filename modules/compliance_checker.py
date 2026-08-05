import re
from typing import List, Dict

def check_clause_compliance(clause: str, clause_type: str) -> Dict[str, str]:
    """
    Evaluates a single clause against legal compliance rules:
    - Governing Law must be Delaware.
    - Notice Period must be 30 days.
    - Confidentiality clause must exist.
    - Liability amount must not exceed $50,000.
    
    Returns:
        Dict[str, str]: Dictionary containing 'Clause', 'Clause Type', 'Status', and 'Reason'.
    """
    text_lower = clause.lower()
    status = "Compliant"
    reasons = []

    # Rule 1: Governing Law must be Delaware
    if clause_type == "Governing Law" or "governing law" in text_lower or "jurisdiction" in text_lower:
        if "delaware" in text_lower:
            reasons.append("Governing law is set to Delaware as required.")
        else:
            found_jurisdiction = None
            for loc in ["new york", "california", "texas", "florida", "london", "uk", "england"]:
                if loc in text_lower:
                    found_jurisdiction = loc.title()
                    break
            if found_jurisdiction:
                status = "Non-Compliant"
                reasons.append(f"Governing law specifies {found_jurisdiction} instead of Delaware.")
            else:
                status = "Non-Compliant"
                reasons.append("Governing law clause does not specify Delaware.")

    # Rule 2: Notice Period must be 30 days
    if "notice" in text_lower and ("day" in text_lower or "days" in text_lower):
        days_match = re.search(r'(\d+)\s*(?:-\s*)?days?', text_lower)
        if days_match:
            days = int(days_match.group(1))
            if days == 30:
                reasons.append("Notice period is set to 30 days as required.")
            else:
                status = "Non-Compliant"
                reasons.append(f"Notice period is {days} days, which violates the required 30-day notice period.")

    # Rule 3: Confidentiality clause presence
    if clause_type == "Confidentiality" or "confidential" in text_lower:
        reasons.append("Confidentiality clause present in contract.")

    # Rule 4: Liability amount must not exceed $50,000
    if clause_type == "Liability" or "liability" in text_lower or "damages" in text_lower:
        amounts = re.findall(r'\$\s*([\d,]+)|\b([\d,]+)\s*(?:dollars|usd)\b', text_lower)
        extracted_nums = []
        for a1, a2 in amounts:
            num_str = (a1 or a2).replace(',', '')
            if num_str.isdigit():
                extracted_nums.append(int(num_str))

        if extracted_nums:
            max_amount = max(extracted_nums)
            if max_amount <= 50000:
                reasons.append(f"Liability amount (${max_amount:,}) does not exceed the $50,000 threshold.")
            else:
                status = "Non-Compliant"
                reasons.append(f"Liability amount (${max_amount:,}) exceeds maximum permitted limit of $50,000.")

    if not reasons:
        reasons.append("Clause meets standard contract guidelines.")

    return {
        "Clause": clause,
        "Clause Type": clause_type,
        "Status": status,
        "Reason": " ".join(reasons)
    }

def evaluate_contract_compliance(classified_clauses: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Evaluates all clauses in a contract for compliance rules, including contract-wide rules.
    """
    results = []
    has_confidentiality = False

    for item in classified_clauses:
        clause_text = item.get("Clause", "")
        clause_type = item.get("Clause Type", "Other / General")

        if clause_type == "Confidentiality" or "confidential" in clause_text.lower():
            has_confidentiality = True

        eval_result = check_clause_compliance(clause_text, clause_type)
        results.append(eval_result)

    # Mandatory Rule 3: Confidentiality clause must exist
    if not has_confidentiality:
        results.append({
            "Clause": "[MANDATORY CONTRACT REQUIREMENT]",
            "Clause Type": "Confidentiality",
            "Status": "Non-Compliant",
            "Reason": "Contract fails compliance: Missing required Confidentiality clause."
        })

    return results
