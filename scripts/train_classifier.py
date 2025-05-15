import os
import sys
import logging
from PIL import Image
import docx
from io import BytesIO

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.model.classifier import DocumentClassifier

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_metadata_from_image(file_path):
    """Extract metadata from an image file."""
    try:
        img = Image.open(file_path)
        # Extract basic image properties as text
        metadata = f"Image format: {img.format}\n"
        metadata += f"Image size: {img.size}\n"
        metadata += f"Color mode: {img.mode}\n"
        metadata += f"Filename features: {os.path.basename(file_path)}\n"
        
        # Add color statistics if available
        if img.mode in ('RGB', 'RGBA'):
            # Calculate average color
            avg_color = tuple(sum(x) // len(x) for x in zip(*img.getdata()))
            metadata += f"Average color (RGB): {avg_color}\n"
        
        return metadata
    except Exception as e:
        logger.error(f"Error extracting metadata from {file_path}: {e}")
        return ""

def get_document_type(filename):
    """Get document type from filename."""
    lower_name = filename.lower()
    if "invoice" in lower_name:
        return "invoice"
    elif "drivers_licen" in lower_name:  # handles both license and licence
        return "drivers_license"
    elif "bank_statement" in lower_name:
        return "bank_statement"
    return "unknown"

def extract_text_from_pdf(file_path):
    """Extract text from PDF file."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read().decode('utf-8', errors='ignore')
            return content
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Extract text from DOCX file."""
    try:
        doc = docx.Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        logger.error(f"Error extracting text from DOCX {file_path}: {e}")
        return ""

def main():
    # Initialize classifier
    classifier = DocumentClassifier()
    
    # Process files
    files_dir = "files"
    texts = []
    labels = []
    
    logger.info("Processing training files...")
    for filename in os.listdir(files_dir):
        if filename.startswith('.'):  # Skip hidden files
            continue
            
        file_path = os.path.join(files_dir, filename)
        doc_type = get_document_type(filename)
        
        if doc_type == "unknown":
            logger.warning(f"Skipping file with unknown type: {filename}")
            continue
        
        logger.info(f"Processing {filename} as {doc_type}")
        
        # Extract text based on file type
        text = ""
        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif filename.lower().endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            text = extract_metadata_from_image(file_path)
        else:
            logger.warning(f"Unsupported file type: {filename}")
            continue
        
        if text:
            texts.append(text)
            labels.append(doc_type)
            logger.info(f"Added {filename} to training set with {len(text)} characters")
        else:
            logger.warning(f"No text extracted from {filename}")
    
    if not texts:
        logger.error("No valid documents found for training")
        return
    
    logger.info(f"Training classifier with {len(texts)} documents:")
    for label in set(labels):
        count = labels.count(label)
        logger.info(f"  - {label}: {count} documents")
    
    # Train classifier
    logger.info("Training classifier...")
    metrics = classifier.train(texts, labels)
    logger.info(f"Training metrics: {metrics}")
    
    # Save models
    os.makedirs("models", exist_ok=True)
    classifier.save(
        "models/classifier.joblib",
        "models/vectorizer.joblib",
        "models/label_encoder.joblib"
    )
    logger.info("Models saved successfully")

if __name__ == '__main__':
    main() 