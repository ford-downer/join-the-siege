from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

class DocumentEmbedder:
    """Generates embeddings for document text using sentence-transformers."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the embedder with a specific model.
        
        Args:
            model_name: Name of the sentence-transformer model to use
        """
        self.model = SentenceTransformer(model_name)
    
    def embed(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for the input text.
        
        Args:
            text: String or list of strings to embed
            
        Returns:
            numpy.ndarray: Document embeddings
        """
        if isinstance(text, str):
            # Split long documents into chunks of ~500 characters
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
            embeddings = self.model.encode(chunks)
            # Average the chunk embeddings
            return np.mean(embeddings, axis=0)
        else:
            return self.model.encode(text)
    
    def get_embedding_dim(self) -> int:
        """Get the dimensionality of the embeddings."""
        return self.model.get_sentence_embedding_dimension() 