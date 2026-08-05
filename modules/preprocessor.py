import re
from collections import Counter

def remove_page_numbers(text: str) -> str:
    """
    Removes common page number patterns and standalone line numbers from text.
    """
    # Patterns matching "Page X of Y", "Page X", "- X -", "X of Y", etc.
    patterns = [
        r'(?i)\bpage\s+\d+(\s+of\s+\d+)?\b',
        r'(?i)\bpage\s*-\s*\d+\s*-\b',
        r'-\s*\d+\s*-',
        r'(?i)\b\d+\s+of\s+\d+\b',
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text)
        
    # Remove standalone digit lines (common page numbers at page headers/footers)
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if not re.match(r'^\s*\d+\s*$', line)]
    return '\n'.join(cleaned_lines)

def remove_repeated_headers_footers(text: str, min_repeat_count: int = 2) -> str:
    """
    Identifies and removes lines that repeat across pages or sections (headers/footers).
    """
    lines = [line.strip() for line in text.split('\n')]
    non_empty_lines = [line for line in lines if line]
    line_counts = Counter(non_empty_lines)
    
    # Lines appearing multiple times with non-trivial length are treated as repeated headers/footers
    repeated_lines = {
        line for line, count in line_counts.items()
        if count >= min_repeat_count and len(line) > 3
    }
    
    cleaned_lines = [line for line in text.split('\n') if line.strip() not in repeated_lines]
    return '\n'.join(cleaned_lines)

def clean_text(text: str) -> str:
    """
    Cleans raw contract text by removing:
    - Extra spaces and tabs
    - Page numbers
    - Repeated headers and footers
    - Multiple redundant newlines
    
    Normalizes whitespace and returns the cleaned text string.
    """
    if not text:
        return ""
        
    # Remove page numbers
    text = remove_page_numbers(text)
    
    # Remove repeated headers and footers
    text = remove_repeated_headers_footers(text)
    
    # Replace tabs with spaces
    text = text.replace('\t', ' ')
    
    # Normalize spaces per line
    lines = text.split('\n')
    cleaned_lines = [re.sub(r' +', ' ', line).strip() for line in lines]
    text = '\n'.join(cleaned_lines)
    
    # Reduce 3 or more consecutive newlines to double newlines (paragraphs)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()
