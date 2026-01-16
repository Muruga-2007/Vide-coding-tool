# File Reader Tools Documentation

This document describes the file reading utilities implemented in `backend/app/tools`. These tools are designed to provide robust, universal file reading capabilities and Google ADK (AI Developer Kit) compatibility.

## Overview

The toolkit consists of two main components:
1.  **`file_reader.py`**: A universal file reader utility that handles text, binary, image, and media files.
2.  **`google_adk_tool.py`**: A wrapper that exposes the file reader as a Google ADK-compatible tool for AI function calling.

---

## 1. Universal File Reader (`file_reader.py`)

### Location
`backend/app/tools/file_reader.py`

### Features
-   **Automatic Type Detection**: Identifies file types based on extensions and MIME types.
-   **Universal Interface**: A single `read()` method that returns structured data appropriate for the file type.
-   **Supported Categories**:
    -   **Text**: `.txt`, `.md`, `.json`, `.py`, `.js`, `.html`, etc. (Returns content as string)
    -   **Images**: `.jpg`, `.png`, `.svg`, etc. (Returns content as base64 string)
    -   **Binary**: `.pdf`, `.zip`, `.exe`, etc. (Returns content as base64 string)
    -   **Media**: `.mp3`, `.mp4`, etc. (Returns metadata, content skipped for performance)

### Usage

#### Using the `FileReader` Class
```python
from backend.app.tools.file_reader import FileReader

# Initialize
reader = FileReader("path/to/file.txt")

# Read file
result = reader.read()

# Access results
print(f"Type: {result['content_type']}")
print(f"Content: {result['content']}")
```

#### Using Convenience Functions
```python
from backend.app.tools.file_reader import read_file, read_text_file

# Quick read with metadata
data = read_file("report.pdf")
print(f"Base64 Data: {data['base64']}")

# Simple text read
text = read_text_file("notes.md")
print(text)
```

### Return Data Structure
The `read()` method returns a dictionary with the following structure:
```json
{
  "filename": "example.txt",
  "path": "/abs/path/to/example.txt",
  "extension": ".txt",
  "mime_type": "text/plain",
  "size_bytes": 1024,
  "content_type": "text",      // 'text', 'image', 'binary', or 'media'
  "content": "File contents...", // String for text, bytes for binary (internal)
  "base64": "..."              // Base64 string for non-text files
}
```

---

## 2. Google ADK Tool Wrapper (`google_adk_tool.py`)

### Location
`backend/app/tools/google_adk_tool.py`

### Purpose
This module wraps the `FileReader` functionality into a format that satisfies the Google AI Developer Kit (ADK) schema for function calling. This allows AI models to easily discover and use the file reading tool.

### Features
-   **Standardized Schema**: usage of `get_tool_definition()` to return the JSON schema required by Google AI.
-   **Simplified Entry Point**: `read_file_tool(file_path, encoding)` function for direct invocation.

### Integration Guide

#### Web/Agent Integration
To register this tool with a Google AI agent:

```python
from backend.app.tools.google_adk_tool import read_file_tool, get_tool_definition

# 1. Get the tool definition
tool_def = get_tool_definition()

# 2. Pass this definition to the LLM/Agent configuration
# ... (Agent configuration code) ...

# 3. When the Agent calls 'read_file_tool', execute:
result = read_file_tool(file_path="/path/requested/by/agent")
```

#### Tool Definition
The tool exposes the following JSON schema:
```json
{
  "name": "read_file_tool",
  "description": "Read any file from the filesystem and return its contents with metadata...",
  "parameters": {
    "type": "object",
    "properties": {
      "file_path": { "type": "string" },
      "encoding": { "type": "string", "default": "utf-8" }
    },
    "required": ["file_path"]
  }
}
```
