import os
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
import uvicorn

from .extractor.pdf import PDFExtractor
from .model.classifier import DocumentClassifier

# Initialize FastAPI app
app = FastAPI(title="Document Classification Service")
security = HTTPBearer()

# Initialize components
pdf_extractor = PDFExtractor()
classifier = DocumentClassifier()

# Load the classifier model
MODEL_PATH = os.getenv("MODEL_PATH", "models/classifier.joblib")
VECTORIZER_PATH = os.getenv("VECTORIZER_PATH", "models/vectorizer.joblib")
LABEL_ENCODER_PATH = os.getenv("LABEL_ENCODER_PATH", "models/label_encoder.joblib")

try:
    classifier.load(MODEL_PATH, VECTORIZER_PATH, LABEL_ENCODER_PATH)
except Exception as e:
    print(f"Warning: Could not load model: {e}")

class ClassificationResponse(BaseModel):
    filename: str
    predicted_class: str
    confidence: float
    error: Optional[str] = None

@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Document classification service is running"}

# API key validation
def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """Verify the API key from the Authorization header."""
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="API key not configured on server"
        )
    if credentials.credentials != api_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return credentials.credentials

@app.post("/classify_file", response_model=ClassificationResponse)
async def classify_file(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    """
    Classify an uploaded document file.
    
    Args:
        file: The document file to classify
        api_key: API key for authentication
        
    Returns:
        ClassificationResponse containing the predicted class and confidence
    """
    try:
        # Validate file format
        if not pdf_extractor.supports_format(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: {file.filename}"
            )
        
        # Extract content
        content = pdf_extractor.extract(file.file)
        if content.get('error'):
            return ClassificationResponse(
                filename=file.filename,
                predicted_class="unknown",
                confidence=0.0,
                error=content['error']
            )
        
        # Get prediction
        predicted_class, confidence = classifier.predict(content['text'])
        
        return ClassificationResponse(
            filename=file.filename,
            predicted_class=predicted_class,
            confidence=confidence
        )
        
    except Exception as e:
        return ClassificationResponse(
            filename=file.filename,
            predicted_class="unknown",
            confidence=0.0,
            error=str(e)
        )

if __name__ == "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True) 