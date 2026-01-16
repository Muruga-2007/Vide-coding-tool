from app.ai_engine.llm_manager import LLMManager
from app.ai_engine.prompt_builder import PromptBuilder
from app.repo.context_builder import ContextBuilder
from app.ai_engine.embeddings import EmbeddingManager
from loguru import logger

# Initialize Singletons
logger.info("Initializing AI Services...")
try:
    llm_manager = LLMManager()
    prompt_builder = PromptBuilder()
    embedding_manager = EmbeddingManager()
    context_builder = ContextBuilder(embedding_manager)
    logger.info("AI Services Initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    raise e
