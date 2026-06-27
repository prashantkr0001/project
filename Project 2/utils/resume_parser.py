import re
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_docx(file) -> str:
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_text(file) -> str:
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        return file.read().decode("utf-8")


def extract_email(text: str) -> str:
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "Not found"


def extract_phone(text: str) -> str:
    match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    return match.group(0) if match else "Not found"


def extract_name(text: str) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines[:5]:
        if re.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+)+$", line):
            return line
    return "Unknown"
