from pathlib import Path
from datetime import datetime   
import hashlib   # For unique document ID

def build_document_metadata(path: str) -> dict:
    
    pdf_path = Path(path)

    doucument_name = pdf_path.name
    doc_id = hashlib.md5(
        str(pdf_path).encode()).hexdigest()
    
    file_size = pdf_path.stat().st_size
    
    ingested_at = datetime.now().isoformat()

    return {
        "document_id": doc_id,
        "document_name": doucument_name,
        "source_path": str(pdf_path),
        "file_size": file_size,
        "ingested_at": ingested_at
    }

