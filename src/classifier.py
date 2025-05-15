import os
import logging
from typing import BinaryIO, Dict, List, Tuple, Optional
import fitz  # PyMuPDF for PDF processing
import pytesseract
from PIL import Image
import io
from transformers import pipeline
import numpy as np
from werkzeug.datastructures import FileStorage
from functools import lru_cache
from langdetect import detect
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ClassificationError(Exception):
    """Base exception for classification errors"""
    pass

class UnsupportedLanguageError(ClassificationError):
    """Exception for non-English content"""
    pass

class EmptyFileError(ClassificationError):
    """Exception for empty files"""
    pass

class FileValidationError(ClassificationError):
    """Exception for file validation errors"""
    pass

class DocumentClassifier:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=3)  # For async processing
        self._initialize_classifier()
        
        # Define document types
        self.document_types = {
            "drivers_licence": "an identification document with personal details",
            "bank_statement": "a document showing bank transactions and balance",
            "invoice": "a document requesting payment for goods or services"
        }

    def _initialize_classifier(self):
        """Initialize the classifier with error handling"""
        try:
            self.classifier = pipeline("zero-shot-classification", 
                                    model="facebook/bart-large-mnli",
                                    device=-1)  # Use CPU for inference
            logger.info("Classifier initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize classifier: {str(e)}")
            raise

    def validate_file(self, file: FileStorage) -> None:
        """Validate file before processing"""
        if not file or not file.filename:
            raise FileValidationError("No file provided")

        # Check file size (10MB limit)
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        if size > 10 * 1024 * 1024:
            raise FileValidationError("File too large (max 10MB)")
        if size == 0:
            raise EmptyFileError("File is empty")

        # Validate file type
        allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png'}
        ext = '.' + file.filename.lower().split('.')[-1] if '.' in file.filename else ''
        if ext not in allowed_extensions:
            raise FileValidationError(f"Unsupported file type. Allowed: {allowed_extensions}")

    def detect_language(self, text: str) -> str:
        """Detect text language"""
        try:
            if not text.strip():
                return "unknown"
            return detect(text)
        except:
            return "unknown"

    async def extract_text(self, file: FileStorage) -> str:
        """Extract text from file asynchronously"""
        try:
            file_bytes = file.read()
            file.seek(0)

            if file.filename.lower().endswith('.pdf'):
                # Run PDF extraction in thread pool
                loop = asyncio.get_event_loop()
                text = await loop.run_in_executor(
                    self.executor,
                    self._extract_pdf_text,
                    file_bytes
                )
                return text
            else:
                # Skip image processing for now
                return ""
        except Exception as e:
            logger.error(f"Text extraction failed: {str(e)}")
            raise ClassificationError(f"Text extraction failed: {str(e)}")

    def _extract_pdf_text(self, file_bytes: bytes) -> str:
        """Extract text from PDF"""
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return text[:100000]  # Limit text length
        except Exception as e:
            logger.error(f"PDF extraction failed: {str(e)}")
            return ""

    async def classify_file(self, file: FileStorage) -> Dict:
        """Classify a file with comprehensive error handling"""
        try:
            # Validate file
            self.validate_file(file)
            
            # First try filename-based classification
            filename_class = self._classify_by_filename(file.filename.lower())
            
            # Extract and classify content
            text = await self.extract_text(file)
            
            # Check language if we have text content
            if text.strip():
                lang = self.detect_language(text)
                if lang != "en" and lang != "unknown":
                    raise UnsupportedLanguageError(
                        "Heron Classifier only supports English at this time"
                    )

            # Classify content if we have text
            content_class, confidence = "unknown", 0.0
            if text.strip():
                try:
                    result = self.classifier(
                        text[:1024],
                        list(self.document_types.keys()),
                        hypothesis_template="This text is from {}."
                    )
                    content_class = result['labels'][0]
                    confidence = result['scores'][0]
                except Exception as e:
                    logger.error(f"Classification failed: {str(e)}")
                    # Fall back to filename classification
                    content_class = "unknown"
                    confidence = 0.0

            # Use content-based classification if confident
            final_class = content_class if confidence > 0.7 else filename_class

            return {
                "classification": final_class,
                "confidence": confidence,
                "method": "content" if confidence > 0.7 else "filename",
                "filename_classification": filename_class,
                "content_classification": content_class
            }

        except UnsupportedLanguageError as e:
            return {
                "error": str(e),
                "classification": "unknown",
                "confidence": 0.0,
                "method": "error"
            }
        except EmptyFileError as e:
            return {
                "error": "Empty File",
                "classification": "unknown",
                "confidence": 0.0,
                "method": "error"
            }
        except FileValidationError as e:
            return {
                "error": str(e),
                "classification": "unknown",
                "confidence": 0.0,
                "method": "error"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "error": "Internal classification error",
                "classification": "unknown",
                "confidence": 0.0,
                "method": "error"
            }

    def _classify_by_filename(self, filename: str) -> str:
        """Basic filename-based classification"""
        if "drivers_license" in filename or "drivers_licence" in filename:
            return "drivers_licence"
        elif "bank_statement" in filename:
            return "bank_statement"
        elif "invoice" in filename:
            return "invoice"
        return "unknown"

# Initialize global classifier instance
classifier = DocumentClassifier()

# Legacy interface
async def classify_file(file: FileStorage) -> str:
    """Legacy interface for backward compatibility"""
    result = await classifier.classify_file(file)
    return result["classification"]

