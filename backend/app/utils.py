import pdfplumber
from docx import Document as DocxDocument
import os

def extract_text_from_pdf(path):
    texts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                texts.append(t)
    return "\n".join(texts)

def extract_text_from_docx(path):
    doc = DocxDocument(path)
    texts = [p.text for p in doc.paragraphs if p.text]
    return "\n".join(texts)

def extract_text(path, filename):
    ext = filename.lower().split('.')[-1]
    if ext == "pdf":
        return extract_text_from_pdf(path)
    elif ext in ("docx","doc"):
        return extract_text_from_docx(path)
    else:
        # fallback - treat as plain text
        try:
            return open(path, encoding="utf-8").read()
        except:
            return ""
