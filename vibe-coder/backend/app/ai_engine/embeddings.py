from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from loguru import logger

class EmbeddingManager:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384 # Dimension for all-MiniLM-L6-v2
        self.index = None
        self.documents = [] # Metadata store

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)

    def create_index(self, documents: List[Dict]):
        """
        documents: List of dicts with 'content' and 'path'
        """
        self.documents = documents
        texts = [doc['content'] for doc in documents]
        
        if not texts:
            logger.warning("No texts to index")
            return

        embeddings = self.generate_embeddings(texts)
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings.astype('float32'))
        logger.info(f"Indexed {len(documents)} documents")

    def search(self, query: str, k: int = 5) -> List[Dict]:
        if not self.index or not self.documents:
            return []
        
        query_vector = self.generate_embeddings([query])
        distances, indices = self.index.search(query_vector.astype('float32'), k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.documents):
                results.append(self.documents[idx])
        
        return results
