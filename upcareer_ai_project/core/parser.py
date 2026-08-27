import re
import pdfplumber
import PyPDF2
from docx import Document

def clean_text(text):
    if not text:
        return ""
    # Strip non-ASCII
    text = text.encode("ascii", "ignore").decode()
    
    # Expand common acronyms
    acronyms = {
        r"\bML\b": "Machine Learning",
        r"\bDL\b": "Deep Learning",
        r"\bNLP\b": "Natural Language Processing",
        r"\bCV\b": "Computer Vision",
        r"\bSE\b": "Software Engineering",
        r"\bCS\b": "Computer Science",
    }
    for acro, expansion in acronyms.items():
        text = re.sub(acro, expansion, text)
        
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def parse_pdf(file_path_or_bytes):
    text = ""
    try:
        # Try pdfplumber first
        with pdfplumber.open(file_path_or_bytes) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception as e:
        # Fallback to PyPDF2
        reader = PyPDF2.PdfReader(file_path_or_bytes)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    return clean_text(text)

def parse_docx(file_path_or_bytes):
    doc = Document(file_path_or_bytes)
    text = " ".join([p.text for p in doc.paragraphs])
    return clean_text(text)

def parse_txt(file_path_or_bytes):
    if hasattr(file_path_or_bytes, 'read'):
        text = file_path_or_bytes.read()
        if isinstance(text, bytes):
            text = text.decode('utf-8', errors='ignore')
    else:
        with open(file_path_or_bytes, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    return clean_text(text)

def parse_document(file_path_or_bytes, filename=""):
    name = filename.lower()
    if name.endswith(".pdf"):
        return parse_pdf(file_path_or_bytes)
    elif name.endswith(".docx"):
        return parse_docx(file_path_or_bytes)
    else:
        # Default to txt
        return parse_txt(file_path_or_bytes)
