# File Reader & Writer Tools Documentation

This document describes the file reading and writing utilities implemented in `backend/app/tools`. These tools are designed to provide robust, universal file operations and Google ADK (AI Developer Kit) compatibility.

## Overview

The toolkit consists of four main components:
1.  **`file_reader.py`**: A universal file reader utility.
2.  **`google_adk_tool.py`**: Google ADK wrapper for the file reader.
3.  **`file_writer.py`**: A universal file writer utility (Write, Append, Replace).
4.  **`google_adk_writer_tool.py`**: Google ADK wrapper for the file writer.

---

## 1. Universal File Reader (`file_reader.py`)

### Location
`backend/app/tools/file_reader.py`

### Features
-   **Automatic Type Detection**: Identifies file types based on extensions and MIME types.
-   **Universal Interface**: A single `read()` method that returns structured data.
-   **Supported Categories**: Text, Images, Binary, Media.

### Usage

```python
from backend.app.tools.file_reader import FileReader, read_file

# Quick read
data = read_file("report.pdf")
print(f"Base64 Data: {data['base64']}")
```

---

## 2. Google ADK Reader Tool (`google_adk_tool.py`)

### Location
`backend/app/tools/google_adk_tool.py`

### Purpose
Exposes `read_file_tool` for AI agent integration.

---

## 3. Universal File Writer (`file_writer.py`)

### Location
`backend/app/tools/file_writer.py`

### Features
-   **Create**: Create new files safely.
-   **Write**: Overwrite existing files.
-   **Append**: Add content to the end of files.
-   **Replace**: Search and replace text content.

### Usage

#### Using the `FileWriter` Class
```python
from backend.app.tools.file_writer import FileWriter

# Write (Overwrite)
FileWriter("log.txt").write("Initial content")

# Append
FileWriter("log.txt").append("\nNew entry", new_line=False)

# Replace
FileWriter("config.py").replace(target="DEBUG = False", replacement="DEBUG = True")
```

#### Using Convenience Functions
```python
from backend.app.tools.file_writer import write_to_file, append_to_file, replace_in_file

write_to_file("data.txt", "Hello World")
append_to_file("data.txt", "Bye World")
replace_in_file("data.txt", "Hello", "Hi")
```

---

## 4. Google ADK Writer Tools (`google_adk_writer_tool.py`)

### Location
`backend/app/tools/google_adk_writer_tool.py`

### Purpose
Exposes file modification capabilities to AI agents via the Google ADK schema.

### Tools Provided
1.  **`write_file_tool`**: Create or overwrite files.
2.  **`append_file_tool`**: Append text to files.
3.  **`replace_in_file_tool`**: Find and replace text patterns.

### Integration
Get definitions using `get_tool_definitions()`:

```python
from backend.app.tools.google_adk_writer_tool import get_tool_definitions

tools = get_tool_definitions()
# Returns list of schemas for write, append, and replace tools
```
