from typing import List, Dict

class PromptBuilder:
    def __init__(self):
        self.base_system_prompt = """You are Vibe Coder, an advanced local-first AI coding assistant. 
You act as a pair programmer, helping the user modify their codebase, fix bugs, and understand code.
You ALWAYS return code changes in a structured format that can be parsed.
Do not delete files without explicit permission.
Respect the existing project structure and style.
"""

    def build_system_prompt(self, context_files: List[Dict] = None) -> str:
        prompt = self.base_system_prompt
        
        if context_files:
            prompt += "\n\n### Context Files:\n"
            for file in context_files:
                prompt += f"\nFile: {file['path']}\n"
                prompt += f"```\n{file['content']}\n```\n"
        
        return prompt

    def build_query(self, user_input: str, additional_context: str = "") -> str:
        query = f"User Request: {user_input}"
        if additional_context:
            query += f"\n\nAdditional Info:\n{additional_context}"
        return query
