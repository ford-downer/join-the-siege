from typing import Dict, List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
import joblib
import logging

logger = logging.getLogger(__name__)

class DocumentClassifier:
    """Document classifier using TF-IDF and RandomForest."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,  # Ignore terms that appear in less than 2 documents
            max_df=0.9  # Ignore terms that appear in more than 90% of documents
        )
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            class_weight='balanced',  # Handle imbalanced classes
            n_jobs=-1
        )
        self.label_encoder = LabelEncoder()
        
    def train(self, 
             texts: List[str], 
             labels: List[str],
             validation_split: float = 0.2) -> Dict[str, float]:
        """
        Train the classifier on document texts.
        
        Args:
            texts: List of document texts
            labels: Document class labels
            validation_split: Fraction of data to use for validation
            
        Returns:
            Dict containing training metrics
        """
        if len(texts) < 2:
            raise ValueError("Need at least 2 documents for training")
            
        if len(set(labels)) < 2:
            raise ValueError("Need at least 2 different classes for training")
        
        # Convert texts to TF-IDF features
        X = self.vectorizer.fit_transform(texts)
        
        # Encode labels
        y = self.label_encoder.fit_transform(labels)
        
        # Split into train/val
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, 
            test_size=validation_split,
            stratify=y,  # Maintain class distribution in split
            random_state=42
        )
        
        # Calculate class weights
        weights = class_weight.compute_class_weight(
            'balanced',
            classes=np.unique(y_train),
            y=y_train
        )
        class_weights = dict(zip(np.unique(y_train), weights))
        
        # Update model with computed weights
        self.model.class_weight = class_weights
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Get validation score
        val_score = self.model.score(X_val, y_val)
        
        # Get feature importance information
        feature_names = self.vectorizer.get_feature_names_out()
        importances = self.model.feature_importances_
        top_features = sorted(zip(importances, feature_names), reverse=True)[:10]
        
        logger.info("Top 10 important features:")
        for importance, feature in top_features:
            logger.info(f"  {feature}: {importance:.4f}")
        
        return {
            'val_accuracy': val_score,
            'n_features': len(feature_names),
            'n_classes': len(self.label_encoder.classes_)
        }
    
    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict document class from text.
        
        Args:
            text: Document text
            
        Returns:
            Tuple of (predicted_class, confidence)
        """
        if not hasattr(self, 'model') or self.model is None:
            raise RuntimeError("Model not trained")
            
        # Convert text to TF-IDF features
        X = self.vectorizer.transform([text])
        
        # Get class probabilities
        probs = self.model.predict_proba(X)[0]
        
        # Get predicted class and confidence
        pred_idx = np.argmax(probs)
        confidence = float(probs[pred_idx])
        pred_class = self.label_encoder.inverse_transform([pred_idx])[0]
        
        return pred_class, confidence
    
    def save(self, model_path: str, vectorizer_path: str, label_encoder_path: str):
        """Save the model components."""
        if not hasattr(self, 'model') or self.model is None:
            raise RuntimeError("Model not trained")
        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)
        joblib.dump(self.label_encoder, label_encoder_path)
    
    def load(self, model_path: str, vectorizer_path: str, label_encoder_path: str):
        """Load the model components."""
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.label_encoder = joblib.load(label_encoder_path) 