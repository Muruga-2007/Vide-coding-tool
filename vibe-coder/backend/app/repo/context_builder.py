from typing import List, Dict
from app.ai_engine.embeddings import EmbeddingManager
from loguru import logger

class ContextBuilder:
    def __init__(self, embedding_manager: EmbeddingManager):
        self.embedding_manager = embedding_manager

    def retrieve_context(self, query: str, max_files: int = 3) -> List[Dict]:
        """
        Retrieve relevant files based on semantic search.
        """
        logger.info(f"Retrieving context for query: {query}")
        relevant_docs = self.embedding_manager.search(query, k=max_files)
        return relevant_docs
