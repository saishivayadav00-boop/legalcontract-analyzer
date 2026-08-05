import re
from typing import List

def segment_clauses(text: str) -> List[str]:
    """
    Segments clean legal contract text into a list of clauses.
    
    Splits text using:
    - Paragraph breaks (\n\n)
    - Legal numbering patterns (1., 1.1, 2., Article I, Section, (a), etc.)
    - Semicolons (;)
    
    Parameters:
        text (str): Preprocessed clean contract text.
        
    Returns:
        List[str]: List of segmented clause strings.
    """
    if not text or not text.strip():
        return []

    # Regex lookahead pattern to match legal headers/numberings at start of lines:
    # - 1., 1.1, 2., 2.1.3
    # - Article I, Article 1, ARTICLE II
    # - Section 1, Section 1.1, SECTION
    # - (a), (b), (1), (i)
    legal_header_pattern = (
        r'(?m)(?=('
        r'^\s*(?:'
        r'Article\s+[IVXLCDM\d]+|'
        r'Section(?:\s+[\d\.]+)?|'
        r'\d+(?:\.\d+)*\.?|'
        r'\([a-zA-Z0-9]+\)'
        r')(?:\s+|\.|$)'
        r'))'
    )

    # Step 1: Split into major paragraph blocks
    paragraph_blocks = text.split('\n\n')
    
    raw_clauses = []
    for block in paragraph_blocks:
        # Split each block on legal numbering markers
        sub_clauses = re.split(legal_header_pattern, block, flags=re.IGNORECASE)
        for sub in sub_clauses:
            if sub and sub.strip():
                raw_clauses.append(sub.strip())

    # Step 2: Split clauses by semicolons (;)
    final_clauses = []
    for clause in raw_clauses:
        if ';' in clause:
            parts = clause.split(';')
            for part in parts:
                cleaned_part = part.strip()
                if cleaned_part:
                    final_clauses.append(cleaned_part)
        else:
            final_clauses.append(clause)

    # Filter out empty or single-character noise
    return [clause for clause in final_clauses if len(clause) > 1]
