import os
import sys
import fitz

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pdf_extractor import extract_text
from modules.preprocessor import clean_text
from modules.clause_segmenter import segment_clauses
from modules.ner_extractor import extract_entities
from modules.clause_classifier import classify_clauses
from modules.compliance_checker import evaluate_contract_compliance
from modules.risk_scoring import calculate_risk_score
from utils.pdf_generator import generate_pdf_report

class SampleFileBuffer:
    def __init__(self, filepath):
        self.name = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            self._bytes = f.read()
        self.size = len(self._bytes)

    def read(self):
        return self._bytes

    def seek(self, pos):
        pass

def run_test_for_file(filepath):
    print("\n" + "="*70)
    print(f" TESTING CONTRACT AUDIT PIPELINE: {os.path.basename(filepath)} ")
    print("="*70)
    
    file_buffer = SampleFileBuffer(filepath)
    file_size_str = f"{file_buffer.size / 1024:.2f} KB"
    
    print(f"[1] Extracting text using PyMuPDF...")
    raw_text = extract_text(file_buffer)
    print(f"    Raw Text Length: {len(raw_text)} characters")
    
    print(f"[2] Cleaning and normalizing text...")
    cleaned_text = clean_text(raw_text)
    
    print(f"[3] Segmenting contract clauses...")
    clauses = segment_clauses(cleaned_text)
    print(f"    Total Clauses Found: {len(clauses)}")
    for i, c in enumerate(clauses, 1):
        print(f"    Clause #{i}: {c[:90]}...")
        
    print(f"[4] Classifying clauses...")
    classified_clauses = classify_clauses(clauses)
    for item in classified_clauses:
        print(f"    [{item['Clause Type']}] -> {item['Clause'][:60]}...")
        
    print(f"[5] Extracting Named Entities (spaCy)...")
    entities = extract_entities(cleaned_text)
    for ent in entities:
        print(f"    • [{ent['Type']}] {ent['Entity']}")
        
    print(f"[6] Evaluating Compliance Rules...")
    compliance_results = evaluate_contract_compliance(classified_clauses)
    for res in compliance_results:
        status_tag = "[COMPLIANT]" if res["Status"] == "Compliant" else "[NON-COMPLIANT]"
        print(f"    {status_tag} ({res['Clause Type']}): {res['Reason']}")
        
    print(f"[7] Calculating Risk Metrics...")
    risk_metrics = calculate_risk_score(compliance_results, len(clauses))
    print(f"    ---------------------------------------------------")
    print(f"    TOTAL CLAUSES:     {risk_metrics['total_clauses']}")
    print(f"    COMPLIANT:         {risk_metrics['compliant']}")
    print(f"    REVIEW:            {risk_metrics['review']}")
    print(f"    HIGH RISK:         {risk_metrics['high_risk']}")
    print(f"    RISK SCORE:        {risk_metrics['risk_score']}% ({risk_metrics['risk_level']})")
    print(f"    ---------------------------------------------------")
    
    print(f"[8] Generating PDF Audit Report...")
    pdf_bytes = generate_pdf_report(
        contract_name=file_buffer.name,
        file_size_str=file_size_str,
        risk_metrics=risk_metrics,
        compliance_results=compliance_results,
        entities=entities,
        classified_clauses=classified_clauses
    )
    print(f"    PDF Report generated successfully ({len(pdf_bytes)} bytes).")
    
    return risk_metrics, compliance_results

if __name__ == "__main__":
    sample_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_contracts")
    comp_file = os.path.join(sample_dir, "compliant_contract.pdf")
    non_comp_file = os.path.join(sample_dir, "non_compliant_contract.pdf")
    
    run_test_for_file(comp_file)
    run_test_for_file(non_comp_file)
