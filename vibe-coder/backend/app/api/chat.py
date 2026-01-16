from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.ai_engine.llm_manager import LLMManager
from app.ai_engine.prompt_builder import PromptBuilder
from app.repo.context_builder import ContextBuilder
from app.ai_engine.embeddings import EmbeddingManager
from app.core.config import settings

router = APIRouter()

# Initialize Singletons (TODO: Use Dep Injection)
llm_manager = LLMManager()
prompt_builder = PromptBuilder()
embedding_manager = EmbeddingManager()
context_builder = ContextBuilder(embedding_manager)

class ChatRequest(BaseModel):
    message: str
    project_path: Optional[str] = None
    history: Optional[List[Dict[str, str]]] = None

@router.post("/query")
async def chat_query(request: ChatRequest):
    # 1. Retrieve Context (only if index exists/project path provided)
    # In a real scenario, we'd ensure index is loaded for this project
    context_files = context_builder.retrieve_context(request.message)
    
    # 2. Build Prompt
    system_prompt = prompt_builder.build_system_prompt(context_files)
    messages = llm_manager.create_messages(system_prompt, request.message, request.history)
    
    # 3. Get Response
    response = await llm_manager.get_response(messages)
    
    return {"response": response, "context": context_files}
