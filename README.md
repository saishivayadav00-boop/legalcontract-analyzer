# Legal Contract Analyzer and Clause Compliance Checker

A Python application built with Streamlit, PyMuPDF, spaCy, Scikit-learn, Pandas, and NumPy for analyzing legal contracts and checking clause compliance.

## Project Structure

```
LegalContractAnalyzer/
│── app.py
│── requirements.txt
│── README.md
│── data/
│── models/
│── utils/
│── modules/
│── sample_contracts/
```

## Tech Stack
- **Python 3.11**
- **Streamlit** - Web UI
- **PyMuPDF (fitz)** - PDF text extraction
- **spaCy** - NLP parsing and named entity recognition
- **Scikit-learn** - Machine learning / classification models
- **Pandas & NumPy** - Data manipulation and numerical operations

## Installation & Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Download spaCy English model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. Run Streamlit App:
   ```bash
   streamlit run app.py
   ```
