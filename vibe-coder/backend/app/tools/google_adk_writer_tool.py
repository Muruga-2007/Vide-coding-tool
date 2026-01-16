# Google ADK Tool Wrapper for FileWriter
"""
Google AI Developer Kit (ADK) tool definition for writing files.
This module provides functions `write_file_tool`, `append_file_tool`, and
`replace_in_file_tool` that conform to the Google function calling schema.
"""

from typing import Dict, Any, Union, List
from pathlib import Path
from .file_writer import FileWriter

def write_file_tool(file_path: Union[str, Path], content: str, 
                   encoding: str = "utf-8", overwrite: bool = True) -> Dict[str, Any]:
    """Write content to a file.
    
    Args:
        file_path: Path to the target file.
        content: The text content to write.
        encoding: File encoding (default: 'utf-8').
        overwrite: Whether to overwrite existing files (default: True).
        
    Returns:
        Dictionary with success status and message.
    """
    try:
        if overwrite:
            success = FileWriter(file_path).write(content, encoding=encoding)
            action = "Overwritten"
        else:
            success = FileWriter(file_path).create(content, overwrite=False, encoding=encoding)
            action = "Created"
            
        return {
            "success": success,
            "message": f"Successfully {action} file: {file_path}",
            "path": str(file_path)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error writing file: {str(e)}",
            "path": str(file_path)
        }

def append_file_tool(file_path: Union[str, Path], content: str, 
                    new_line: bool = True, encoding: str = "utf-8") -> Dict[str, Any]:
    """Append content to a file.
    
    Args:
        file_path: Path to the target file.
        content: The text content to append.
        new_line: Add a newline before content (default: True).
        encoding: File encoding (default: 'utf-8').
        
    Returns:
        Dictionary with success status and message.
    """
    try:
        success = FileWriter(file_path).append(content, new_line=new_line, encoding=encoding)
        return {
            "success": success,
            "message": f"Successfully appended to file: {file_path}",
            "path": str(file_path)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error appending to file: {str(e)}",
            "path": str(file_path)
        }

def replace_in_file_tool(file_path: Union[str, Path], target: str, replacement: str, 
                        count: int = -1, encoding: str = "utf-8") -> Dict[str, Any]:
    """Replace text in a file.
    
    Args:
        file_path: Path to the target file.
        target: Text to search for.
        replacement: Text to replace it with.
        count: Max replacements (-1 for all).
        encoding: File encoding.
        
    Returns:
        Dictionary with success status and message.
    """
    try:
        changed = FileWriter(file_path).replace(target, replacement, count=count, encoding=encoding)
        return {
            "success": True,
            "changed": changed,
            "message": f"Replacement {'successful' if changed else 'completed (no changes)'} in: {file_path}",
            "path": str(file_path)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error replacing in file: {str(e)}",
            "path": str(file_path)
        }

def get_tool_definitions() -> List[Dict[str, Any]]:
    """Return Google ADK tool definitions for writing tools."""
    return [
        {
            "name": "write_file_tool",
            "description": "Create or overwrite a file with text content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": { "type": "string", "description": "Path to the file." },
                    "content": { "type": "string", "description": "Content to write." },
                    "overwrite": { "type": "boolean", "default": True, "description": "Overwrite if exists." }
                },
                "required": ["file_path", "content"]
            }
        },
        {
            "name": "append_file_tool",
            "description": "Append text content to the end of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": { "type": "string", "description": "Path to the file." },
                    "content": { "type": "string", "description": "Content to append." },
                    "new_line": { "type": "boolean", "default": True, "description": "Add newline prefix." }
                },
                "required": ["file_path", "content"]
            }
        },
        {
            "name": "replace_in_file_tool",
            "description": "Replace specific text patterns in a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": { "type": "string", "description": "Path to the file." },
                    "target": { "type": "string", "description": "Text string to find." },
                    "replacement": { "type": "string", "description": "Text string to replace with." }
                },
                "required": ["file_path", "target", "replacement"]
            }
        }
    ]
