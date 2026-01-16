# Google ADK Tool Wrapper for FileReader
"""
Google AI Developer Kit (ADK) tool definition for reading files.
This module provides a function `read_file_tool` that conforms to the Google
function calling schema. It uses the existing `FileReader` utility to read any
supported file type and returns a structured dictionary.
"""

from typing import Dict, Any, Union
from pathlib import Path

# Import the existing FileReader implementation
from .file_reader import FileReader


def read_file_tool(file_path: Union[str, Path], encoding: str = "utf-8") -> Dict[str, Any]:
    """Read a file and return its contents with metadata.

    This function is designed to be used as a Google ADK tool. The return value
    matches the expected JSON schema for function calling.

    Args:
        file_path: Path to the file to read.
        encoding: Text encoding to use for text files (default: "utf-8").

    Returns:
        A dictionary containing file metadata and content. For binary files,
        the content is base64‑encoded.
    """
    reader = FileReader(file_path)
    return reader.read(encoding=encoding)


def get_tool_definition() -> Dict[str, Any]:
    """Return the Google ADK tool definition for `read_file_tool`.

    The definition follows the schema required by Google AI function calling:
    - name: The function name.
    - description: Human‑readable description.
    - parameters: JSON Schema describing the input parameters.
    """
    return {
        "name": "read_file_tool",
        "description": "Read any file from the filesystem and return its contents with metadata. Supports text, image, binary, and media files.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute or relative path to the file to be read."
                },
                "encoding": {
                    "type": "string",
                    "description": "Encoding to use for text files (default: 'utf-8').",
                    "default": "utf-8"
                }
            },
            "required": ["file_path"]
        }
    }

# Example usage (not executed when imported as a tool)
if __name__ == "__main__":
    import json, sys
    if len(sys.argv) < 2:
        print("Usage: python google_adk_tool.py <file_path> [encoding]")
        sys.exit(1)
    path = sys.argv[1]
    enc = sys.argv[2] if len(sys.argv) > 2 else "utf-8"
    result = read_file_tool(path, encoding=enc)
    print(json.dumps(result, indent=2, default=str))
