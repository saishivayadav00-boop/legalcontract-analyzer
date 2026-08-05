import fitz  # PyMuPDF
from typing import Dict, List, Any

def generate_pdf_report(
    contract_name: str,
    file_size_str: str,
    risk_metrics: Dict[str, Any],
    compliance_results: List[Dict[str, str]],
    entities: List[Dict[str, str]],
    classified_clauses: List[Dict[str, str]]
) -> bytes:
    """
    Generates a PDF Audit Report using PyMuPDF.
    
    Includes:
    - Contract Name & File Size
    - Extracted Metadata & Entities
    - Executive Summary & Risk Score
    - Clause Classification Overview
    - Detailed Compliance Audit Table Results
    
    Returns:
        bytes: PDF binary buffer ready for Streamlit st.download_button.
    """
    doc = fitz.open()
    
    # Theme colors
    navy_color = (0.08, 0.16, 0.28)
    text_color = (0.2, 0.2, 0.2)
    green_color = (0.08, 0.5, 0.24)
    red_color = (0.75, 0.11, 0.11)
    yellow_color = (0.65, 0.45, 0.05)
    
    # -------------------------------------------------------------
    # PAGE 1: EXECUTIVE SUMMARY & METADATA
    # -------------------------------------------------------------
    page = doc.new_page(width=595, height=842) # A4 size
    
    # Header Banner
    banner_rect = fitz.Rect(30, 30, 565, 90)
    page.draw_rect(banner_rect, color=navy_color, fill=navy_color)
    page.insert_textbox(
        banner_rect,
        "LEGAL CONTRACT AUDIT REPORT",
        fontsize=18,
        color=(1, 1, 1),
        align=fitz.TEXT_ALIGN_CENTER
    )
    
    y = 115
    # 1. Metadata Section
    page.insert_text((30, y), "1. Contract Metadata", fontsize=13, color=navy_color)
    y += 20
    page.insert_text((45, y), f"Contract Name:  {contract_name}", fontsize=10.5, color=text_color)
    y += 15
    page.insert_text((45, y), f"File Size:      {file_size_str}", fontsize=10.5, color=text_color)
    y += 15
    page.insert_text((45, y), f"Total Clauses:  {risk_metrics.get('total_clauses', 0)}", fontsize=10.5, color=text_color)
    
    y += 30
    # 2. Executive Summary & Risk Score
    page.insert_text((30, y), "2. Executive Risk Summary", fontsize=13, color=navy_color)
    y += 25
    
    score = risk_metrics.get("risk_score", 0.0)
    level = risk_metrics.get("risk_level", "Low Risk")
    score_color = green_color if score < 15 else (yellow_color if score < 40 else red_color)
    
    page.insert_text((45, y), f"Risk Score: {score:.1f}% ({level})", fontsize=13, color=score_color)
    y += 20
    page.insert_text((45, y), f"• Compliant Clauses:       {risk_metrics.get('compliant', 0)}", fontsize=10.5, color=text_color)
    y += 15
    page.insert_text((45, y), f"• Clauses Needing Review:  {risk_metrics.get('review', 0)}", fontsize=10.5, color=text_color)
    y += 15
    page.insert_text((45, y), f"• High Risk Violations:    {risk_metrics.get('high_risk', 0)}", fontsize=10.5, color=text_color)
    
    y += 30
    # 3. Extracted Named Entities
    page.insert_text((30, y), "3. Extracted Metadata & Named Entities", fontsize=13, color=navy_color)
    y += 20
    
    if entities:
        for ent in entities[:10]:
            y += 14
            if y > 780:
                page = doc.new_page(width=595, height=842)
                y = 50
            page.insert_text((45, y), f"• [{ent.get('Type')}] {ent.get('Entity')}", fontsize=9.5, color=text_color)
    else:
        page.insert_text((45, y + 15), "No named entities detected.", fontsize=9.5, color=text_color)

    # -------------------------------------------------------------
    # PAGE 2+: COMPLIANCE AUDIT RESULTS
    # -------------------------------------------------------------
    page = doc.new_page(width=595, height=842)
    y = 50
    page.insert_text((30, y), "4. Compliance Audit Results", fontsize=13, color=navy_color)
    y += 25
    
    for idx, item in enumerate(compliance_results, 1):
        clause_type = item.get("Clause Type", "General")
        status = item.get("Status", "Compliant")
        reason = item.get("Reason", "")
        clause_text = item.get("Clause", "")[:130] + "..." if len(item.get("Clause", "")) > 130 else item.get("Clause", "")
        
        status_color = green_color if status == "Compliant" else red_color
        
        if y > 750:
            page = doc.new_page(width=595, height=842)
            y = 50
            
        page.insert_text((40, y), f"Clause #{idx} [{clause_type}] - Status: {status.upper()}", fontsize=10.5, color=status_color)
        y += 14
        page.insert_text((50, y), f"Text: {clause_text}", fontsize=8.5, color=text_color)
        y += 14
        page.insert_text((50, y), f"Reason: {reason}", fontsize=9, color=text_color)
        y += 22

    # -------------------------------------------------------------
    # PAGE 3+: CLAUSE CLASSIFICATION OVERVIEW
    # -------------------------------------------------------------
    page = doc.new_page(width=595, height=842)
    y = 50
    page.insert_text((30, y), "5. Clause Classification Overview", fontsize=13, color=navy_color)
    y += 25
    
    for idx, item in enumerate(classified_clauses, 1):
        c_text = item.get("Clause", "")[:140] + "..." if len(item.get("Clause", "")) > 140 else item.get("Clause", "")
        c_type = item.get("Clause Type", "Other")
        
        if y > 770:
            page = doc.new_page(width=595, height=842)
            y = 50
            
        page.insert_text((40, y), f"{idx}. [{c_type}]", fontsize=10, color=navy_color)
        y += 13
        page.insert_text((50, y), f"{c_text}", fontsize=8.5, color=text_color)
        y += 18


    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes
