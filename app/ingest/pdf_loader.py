from pathlib import Path
from pypdf import PdfReader
#from app.core.types import Page
from app.core.types import Page
from app.ingest.clean import clean_text


def load_pdf(path: str) -> list[Page]:
    """
    Reads a PDF file and returns a list of pages.
    Each page dict contains:
      - page_number
      - text
      - source_path
    """
    pdf_path = Path(path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"File {pdf_path} does not exist.")

    reader = PdfReader(str(pdf_path))
    pages_data: list[Page] = []

    for i, page in enumerate(reader.pages):
        text = clean_text(page.extract_text()) or ""
        if not text.strip():
            continue  
        pages_data.append(
            Page(
                page_number=i + 1,
                text=text,
                source_path=str(pdf_path),
                char_count=len(text),
                is_empty=len(text.strip()) == 0
            )
        )
    return pages_data