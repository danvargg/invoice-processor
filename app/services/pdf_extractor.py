from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from a PDF file uploaded via FastAPI.
    `pdf_file` is typically an UploadFile object.
    """
    pdf_reader = PdfReader(pdf_file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
