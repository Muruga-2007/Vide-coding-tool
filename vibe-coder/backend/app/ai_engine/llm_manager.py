from typing import Any, List, Optional, AsyncGenerator
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage, BaseMessage
from pydantic import BaseModel
from loguru import logger
import os

from app.core.config import settings

class LLMConfig(BaseModel):
    base_url: str = "http://localhost:11434/v1" # Default to Ollama
    api_key: str = "sk-xxx" # Not used for local, but required by client
    model: str = "llama3" # Default model
    temperature: float = 0.7

class LLMManager:
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self.llm = ChatOpenAI(
            base_url=self.config.base_url,
            api_key=self.config.api_key,
            model=self.config.model,
            temperature=self.config.temperature,
            streaming=True
        )

    async def stream_response(self, messages: List[BaseMessage]) -> AsyncGenerator[str, None]:
        try:
            async for chunk in self.llm.astream(messages):
                yield chunk.content
        except Exception as e:
            logger.error(f"LLM Stream Error: {e}")
            yield f"Error: {str(e)}"

    async def get_response(self, messages: List[BaseMessage]) -> str:
        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM Invoice Error: {e}")
            return f"Error: {str(e)}"
            
    def create_messages(self, system_prompt: str, user_query: str, history: List[Dict[str, str]] = None) -> List[BaseMessage]:
        msgs = [SystemMessage(content=system_prompt)]
        if history:
            for h in history:
                if h["role"] == "user":
                    msgs.append(HumanMessage(content=h["content"]))
                elif h["role"] == "assistant":
                    msgs.append(AIMessage(content=h["content"]))
        msgs.append(HumanMessage(content=user_query))
        return msgs
