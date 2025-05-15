import pytest
from fastapi.testclient import TestClient
import numpy as np
from src.embedding.embedder import DocumentEmbedder
from src.model.classifier import DocumentClassifier
from src.api import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def embedder():
    return DocumentEmbedder()

@pytest.fixture
def classifier():
    return DocumentClassifier()

def test_embedder():
    """Test document embedding generation."""
    embedder = DocumentEmbedder()
    text = "This is a test document"
    embedding = embedder.embed(text)
    
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == (embedder.get_embedding_dim(),)

def test_classifier_training():
    """Test classifier training."""
    classifier = DocumentClassifier()
    
    # Generate dummy data
    embeddings = np.random.randn(100, 384)  # 384 is embedding dim for MiniLM
    labels = ["invoice", "receipt"] * 50
    
    metrics = classifier.train(embeddings, labels)
    assert "val_loss" in metrics
    
    # Test prediction
    test_embedding = np.random.randn(384)
    pred_class, confidence = classifier.predict(test_embedding)
    
    assert pred_class in ["invoice", "receipt"]
    assert 0 <= confidence <= 1

def test_api_no_auth(client):
    """Test API endpoint without authentication."""
    response = client.post("/classify_file")
    assert response.status_code == 403

def test_api_invalid_file(client, monkeypatch):
    """Test API endpoint with invalid file."""
    monkeypatch.setenv("API_KEY", "test-key")
    
    headers = {"Authorization": "Bearer test-key"}
    files = {"file": ("test.txt", b"test content", "text/plain")}
    
    response = client.post("/classify_file", headers=headers, files=files)
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"] 