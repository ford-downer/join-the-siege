# Document Classification Service

A Flask-based service for classifying documents (invoices, bank statements, and driver's licenses) using machine learning.

## Features

- Supports multiple file formats (PDF, DOCX, JPG)
- High accuracy document classification (85-93% confidence on test set)
- Pre-trained model included
- Simple REST API
- Batch processing capability
- Easy to set up and use
- Comprehensive test suite

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd document-classifier
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Start the server:
```bash
python src/app.py
```

The server will start on http://localhost:8000

## Using the Service

### Single File Classification
Send a POST request to `/classify_file` with a file:

```bash
curl -X POST http://localhost:8000/classify_file \
  -F "file=@path/to/your/document.pdf"
```

Response:
```json
{
  "file_class": "invoice",
  "confidence": 0.86
}
```

### Batch Processing
Use the included batch processing script to classify multiple files:

```bash
python batch_process.py
```

The script will process all supported files in the `files` directory and display results in a table format.

## Testing

The project includes a comprehensive test suite covering both unit tests and integration tests.

### Running Tests

To run all tests:
```bash
python run_tests.py
```

### Test Coverage

The test suite includes:

1. Unit Tests (`tests/test_classifier.py`):
   - Classifier initialization
   - Document type classification accuracy
   - Empty text handling
   - Invalid text handling
   - Confidence score validation

2. Integration Tests (`tests/test_api.py`):
   - API endpoints
   - File upload handling
   - Error cases
   - Response format
   - Classification accuracy

### Adding New Tests

To add new tests:
1. Create a new test file in the `tests` directory
2. Follow the existing test patterns
3. Run the test suite to verify

## Pre-trained Model

This repository includes a pre-trained model in the `models` directory:
- `classifier.joblib`: The main classification model
- `vectorizer.joblib`: Text vectorizer
- `label_encoder.joblib`: Label encoder
- `classifier.lgb`: LightGBM model file

The model has been trained on a diverse dataset of:
- Invoices
- Bank Statements
- Driver's Licenses

Performance metrics from testing:
- DOCX files: 84-93% confidence
- PDF files: 65-91% confidence
- JPG files: ~61% confidence (driver's licenses only)

## Project Structure

```
.
├── src/
│   ├── app.py              # Flask application
│   └── model/             
│       └── classifier.py   # Document classifier
├── models/                # Pre-trained model files
├── files/                 # Test files directory
├── tests/                 # Test suite
│   ├── test_classifier.py # Unit tests
│   └── test_api.py       # Integration tests
├── batch_process.py       # Batch processing script
├── run_tests.py          # Test runner
└── requirements.txt       # Python dependencies
```

## Development

To create new test files:
```bash
python create_test_files.py
```

## Requirements

All dependencies are listed in `requirements.txt`. Key packages:
- Flask
- python-docx
- scikit-learn
- transformers
- PyMuPDF
- numpy
- pandas

## License

This project is licensed under the MIT License. 
