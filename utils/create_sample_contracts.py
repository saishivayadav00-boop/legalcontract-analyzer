import os
import fitz  # PyMuPDF

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_contracts")

COMPLIANT_TEXT = """MASTER SERVICES AGREEMENT (COMPLIANT SAMPLE)

1. DEFINITIONS AND PARTIES
This Master Services Agreement ("Agreement") is entered into by and between Acme Tech Solutions LLC ("Company") and Global Ventures Inc ("Client") as of January 15, 2025.

2. CONFIDENTIALITY OBLIGATIONS
Receiving Party agrees to maintain all Confidential Information and proprietary trade secrets in strict confidence and shall not disclose such information to any third party without prior written consent.

3. TERMINATION AND NOTICE
Either party may terminate this Agreement upon 30 days written notice to the other party in the event of a material breach.

4. LIMITATION OF LIABILITY
The maximum aggregate monetary liability of Provider under this Agreement shall not exceed $25,000 USD.

5. GOVERNING LAW AND JURISDICTION
This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to conflict of law principles.
"""

NON_COMPLIANT_TEXT = """VENDOR SERVICE CONTRACT (NON-COMPLIANT SAMPLE)

1. SERVICES AND SCOPE
This Service Agreement is made between Apex Systems Inc and Delta Corp on August 1, 2025.

2. TERMINATION AND CANCELLATION
Either party may terminate this agreement upon 60 days written notice to the other party.

3. LIMITATION OF LIABILITY
In no event shall seller's maximum liability under this contract exceed $250,000 USD for any and all claims.

4. GOVERNING LAW AND VENUE
This contract is governed by and construed in accordance with the laws of the State of New York, and disputes shall be heard in New York courts.
"""

def create_sample_pdfs():
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    
    comp_path = os.path.join(SAMPLE_DIR, "compliant_contract.pdf")
    non_comp_path = os.path.join(SAMPLE_DIR, "non_compliant_contract.pdf")
    
    # Create Compliant PDF
    doc1 = fitz.open()
    page1 = doc1.new_page()
    page1.insert_textbox(fitz.Rect(40, 40, 555, 780), COMPLIANT_TEXT, fontsize=11)
    doc1.save(comp_path)
    doc1.close()
    print(f"Created Compliant Sample Contract at: {comp_path}")
    
    # Create Non-Compliant PDF
    doc2 = fitz.open()
    page2 = doc2.new_page()
    page2.insert_textbox(fitz.Rect(40, 40, 555, 780), NON_COMPLIANT_TEXT, fontsize=11)
    doc2.save(non_comp_path)
    doc2.close()
    print(f"Created Non-Compliant Sample Contract at: {non_comp_path}")

if __name__ == "__main__":
    create_sample_pdfs()
