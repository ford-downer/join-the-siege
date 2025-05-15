import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from flask import Flask, request, jsonify
import docx
from io import BytesIO
import logging

from src.model.classifier import DocumentClassifier

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize classifier
classifier = DocumentClassifier()

# Load the classifier model
MODEL_PATH = os.path.join(project_root, "models", "classifier.joblib")
VECTORIZER_PATH = os.path.join(project_root, "models", "vectorizer.joblib")
LABEL_ENCODER_PATH = os.path.join(project_root, "models", "label_encoder.joblib")

try:
    classifier.load(MODEL_PATH, VECTORIZER_PATH, LABEL_ENCODER_PATH)
    logger.info("Classifier loaded successfully")
except Exception as e:
    logger.error(f"Error loading classifier: {e}")

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_docx(file_stream):
    doc = docx.Document(BytesIO(file_stream.read()))
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

def extract_text(file):
    """Extract text from various file types."""
    if file.filename.lower().endswith('.docx'):
        return extract_text_from_docx(file)
    elif file.filename.lower().endswith('.pdf'):
        # Use the text extraction from classifier
        return file.read().decode('utf-8', errors='ignore')
    else:
        return ""

@app.route('/')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed"}), 400

    try:
        # Extract text from file
        text = extract_text(file)
        
        # Get classification
        predicted_class, confidence = classifier.predict(text)
        
        return jsonify({
            "file_class": predicted_class,
            "confidence": confidence
        }), 200
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        logger.info("Starting the server...")
        app.run(debug=True, port=8000)
    except Exception as e:
        logger.critical(f"Failed to start server: {str(e)}")
        raise
