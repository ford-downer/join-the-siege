from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Any

class BaseExtractor(ABC):
    """Base class for all content extractors."""
    
    @abstractmethod
    def extract(self, file: BinaryIO) -> Dict[str, Any]:
        """
        Extract content and metadata from a file.
        
        Args:
            file: A file-like object containing the document
            
        Returns:
            Dict containing:
                - text: str, The extracted text content
                - metadata: Dict, Any relevant metadata
                - error: Optional[str], Error message if extraction failed
        """
        pass

    @abstractmethod
    def supports_format(self, filename: str) -> bool:
        """
        Check if this extractor supports the given file format.
        
        Args:
            filename: Name of the file to check
            
        Returns:
            bool: True if this extractor can handle the file format
        """
        pass 