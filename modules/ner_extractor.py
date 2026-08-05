import re
from typing import List, Dict

try:
    import spacy
except ImportError:
    spacy = None

_nlp = None

def get_spacy_model():
    """
    Attempts to load the spaCy 'en_core_web_sm' model.
    Returns None if unavailable or download fails.
    """
    global _nlp, spacy
    if _nlp is not None:
        return _nlp

    if spacy is not None:
        try:
            _nlp = spacy.load("en_core_web_sm")
            return _nlp
        except Exception:
            try:
                import spacy.cli
                spacy.cli.download("en_core_web_sm")
                _nlp = spacy.load("en_core_web_sm")
                return _nlp
            except Exception:
                pass
    return None

def fallback_regex_ner(text: str) -> List[Dict[str, str]]:
    """
    Fallback NER using pattern matching when spaCy model is unavailable offline.
    """
    entities = []
    seen = set()

    # Rule patterns for target entity categories
    patterns = [
        ("Organization", r'\b[A-Z][A-Za-z0-9\s,&]+(?:LLC|Inc|Corp|Corporation|Ltd|Solutions|Systems|Ventures|Group)\b'),
        ("Date", r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b'),
        ("Money", r'\$\s*[\d,]+(?:\.\d{2})?|\b[\d,]+\s*(?:dollars|usd|USD)\b'),
        ("Location", r'\bState of [A-Z][a-z]+\b|\b(?:Delaware|New York|California|Texas|Florida|London|UK|Delaware)\b'),
        ("Person", r'\b(?:Mr\.|Ms\.|Dr\.)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b')
    ]

    for entity_type, regex_pattern in patterns:
        matches = re.finditer(regex_pattern, text)
        for match in matches:
            val = match.group(0).strip()
            key = (val.lower(), entity_type)
            if key not in seen and len(val) > 1:
                seen.add(key)
                entities.append({
                    "Entity": val,
                    "Type": entity_type,
                    "Value": val
                })

    return entities

def extract_entities(text: str) -> List[Dict[str, str]]:
    """
    Extracts named entities (Organization, Date, Money, Location, Person).
    Uses spaCy if available, with an automatic regex fallback.
    """
    if not text or not text.strip():
        return []

    nlp = get_spacy_model()
    if nlp is not None:
        doc = nlp(text)
        target_labels = {
            "ORG": "Organization",
            "DATE": "Date",
            "MONEY": "Money",
            "GPE": "Location",
            "LOC": "Location",
            "PERSON": "Person"
        }
        entities = []
        seen = set()
        for ent in doc.ents:
            if ent.label_ in target_labels:
                val = ent.text.strip()
                entity_type = target_labels[ent.label_]
                key = (val.lower(), entity_type)
                if key not in seen and len(val) > 1:
                    seen.add(key)
                    entities.append({
                        "Entity": val,
                        "Type": entity_type,
                        "Value": val
                    })
        if entities:
            return entities

    # Fallback to regex pattern matching
    return fallback_regex_ner(text)
