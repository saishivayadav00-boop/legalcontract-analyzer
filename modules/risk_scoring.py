from typing import List, Dict, Any

def calculate_risk_score(compliance_results: List[Dict[str, str]], total_clauses_count: int = None) -> Dict[str, Any]:
    """
    Calculates legal contract risk metrics using the formula:
    Risk Score = (Non-Compliant Clauses / Total Clauses) * 100
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - 'total_clauses': Total Clauses count
            - 'compliant': Compliant clauses count
            - 'review': Clauses requiring Review count
            - 'high_risk': High Risk clauses count
            - 'risk_score': Calculated Risk Score percentage
            - 'risk_level': Risk assessment category ('Low Risk', 'Medium Risk', 'High Risk')
    """
    if not compliance_results:
        return {
            "total_clauses": 0,
            "compliant": 0,
            "review": 0,
            "high_risk": 0,
            "risk_score": 0.0,
            "risk_level": "Low Risk"
        }

    compliant_count = sum(1 for item in compliance_results if item.get("Status") == "Compliant")
    non_compliant_count = sum(1 for item in compliance_results if item.get("Status") == "Non-Compliant")
    
    total_count = total_clauses_count if (total_clauses_count and total_clauses_count > 0) else len(compliance_results)
    
    # Formula: Risk Score = (Non-Compliant Clauses / Total Clauses) * 100
    risk_score = (non_compliant_count / total_count * 100.0) if total_count > 0 else 0.0
    
    # Review: non-compliant clauses that need manual legal review
    review_count = non_compliant_count
    
    # High Risk: critical rule violations (liability exceedance, missing confidentiality, jurisdiction mismatch)
    high_risk_count = 0
    for item in compliance_results:
        if item.get("Status") == "Non-Compliant":
            reason = item.get("Reason", "").lower()
            if "exceeds" in reason or "missing" in reason or "instead of delaware" in reason:
                high_risk_count += 1
            else:
                high_risk_count += 1

    if risk_score >= 40.0:
        risk_level = "High Risk"
    elif risk_score >= 15.0:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    return {
        "total_clauses": total_count,
        "compliant": compliant_count,
        "review": review_count,
        "high_risk": high_risk_count,
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level
    }
