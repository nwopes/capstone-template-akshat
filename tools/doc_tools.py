import os

try:
    from docx import Document
except ImportError:
    Document = None

try:
    from reportlab.pdfgen import canvas
except ImportError:
    canvas = None

def write_docx(text: str, out_path: str) -> str:
    """
    Creates a simple DOCX with python-docx containing `text` and returns the path.
    If python-docx is not installed at runtime, raise a clear error message.
    """
    if Document is None:
        raise ImportError("python-docx is not installed. Please install it to use write_docx.")
    
    print(f"Writing DOCX to: {out_path}")
    doc = Document()
    doc.add_paragraph(text)
    doc.save(out_path)
    return out_path

def write_pdf(text: str, out_path: str) -> str:
    """
    Creates a simple PDF using reportlab with `text` and returns the path.
    If reportlab missing, raise a clear error.
    """
    if canvas is None:
        raise ImportError("reportlab is not installed. Please install it to use write_pdf.")
    
    print(f"Writing PDF to: {out_path}")
    c = canvas.Canvas(out_path)
    # Simple text rendering
    y = 800
    for line in text.split('\n'):
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    return out_path

def export_signature_pdf(draft_text: str, out_path: str) -> str:
    """
    Placeholder that writes a PDF and returns path + prints "Signature PDF created (placeholder)".
    """
    print("Signature PDF created (placeholder)")
    return write_pdf(draft_text, out_path)
