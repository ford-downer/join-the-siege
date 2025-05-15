from typing import BinaryIO, Dict, Any
import PyPDF2
from .base import BaseExtractor

class PDFExtractor(BaseExtractor):
    """Extracts content from PDF files."""
    
    def supports_format(self, filename: str) -> bool:
        return filename.lower().endswith('.pdf')
    
    def extract(self, file: BinaryIO) -> Dict[str, Any]:
        try:
            reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Get metadata
            metadata = {
                'page_count': len(reader.pages),
                'is_encrypted': reader.is_encrypted,
            }
            
            if hasattr(reader.metadata, 'title'):
                metadata['title'] = reader.metadata.get('/Title', '')
            if hasattr(reader.metadata, 'author'):
                metadata['author'] = reader.metadata.get('/Author', '')
            
            return {
                'text': text.strip(),
                'metadata': metadata,
                'error': None
            }
            
        except Exception as e:
            return {
                'text': '',
                'metadata': {},
                'error': f"Failed to extract PDF content: {str(e)}"
            } 