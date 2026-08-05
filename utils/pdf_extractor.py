try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


def extract_text(uploaded_file) -> str:
    """
    Extracts text from a PDF file buffer using PyMuPDF, preserving page order.
    
    Parameters:
        uploaded_file: Streamlit UploadedFile or file-like object containing PDF bytes.
        
    Returns:
        str: Extracted text combined from all pages in order.
    """
    if fitz is None:
        raise ImportError("PyMuPDF ('fitz') is not installed. Please run 'pip install pymupdf'.")
        
    # Read byte content from uploaded file
    file_bytes = uploaded_file.read()

    # Reset file pointer so file object can be reused if needed
    uploaded_file.seek(0)
    
    # Open document from memory stream
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    
    pages_text = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        pages_text.append(text)
        
    doc.close()
    
    return "\n\n".join(pages_text)
