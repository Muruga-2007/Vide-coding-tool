"""
Universal File Writer Utility

This module provides functionality to Create, Write, Replace, and Append to files.
It handles both text and binary files.
"""

import os
from pathlib import Path
from typing import Union, List, Optional
import base64

class FileWriter:
    """Universal file writer that handles multiple file operations"""

    def __init__(self, file_path: Union[str, Path]):
        """
        Initialize the FileWriter with a file path.
        
        Args:
            file_path: Path to the file to operate on
        """
        self.file_path = Path(file_path)

    def create(self, content: Union[str, bytes] = "", overwrite: bool = False, encoding: str = 'utf-8') -> bool:
        """
        Create a new file with optional initial content.
        
        Args:
            content: Initial content (string or bytes)
            overwrite: If True, overwrite existing file. If False, raise FileExistsError if file exists.
            encoding: Encoding for text content (default: utf-8)
            
        Returns:
            True if successful
        """
        if self.file_path.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {self.file_path}")
        
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        return self._write_content(content, mode='w', encoding=encoding)

    def write(self, content: Union[str, bytes], encoding: str = 'utf-8') -> bool:
        """
        Write content to file (overwrites existing content).
        
        Args:
            content: Content to write (string or bytes)
            encoding: Encoding for text content (default: utf-8)
            
        Returns:
            True if successful
        """
        return self._write_content(content, mode='w', encoding=encoding)

    def append(self, content: Union[str, bytes], new_line: bool = False, encoding: str = 'utf-8') -> bool:
        """
        Append content to the end of the file.
        
        Args:
            content: Content to append (string or bytes)
            new_line: If True, add a newline character before content (text mode only)
            encoding: Encoding for text content (default: utf-8)
            
        Returns:
            True if successful
        """
        if new_line and isinstance(content, str):
            content = "\n" + content
            
        return self._write_content(content, mode='a', encoding=encoding)

    def replace(self, target: str, replacement: str, count: int = -1, encoding: str = 'utf-8') -> bool:
        """
        Replace specific text content within the file.
        
        Args:
            target: The string to search for
            replacement: The string to replace it with
            count: Maximum number of occurrences to replace (-1 for all)
            encoding: Encoding for text content
            
        Returns:
            True if modifications were made, False otherwise
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        try:
            with open(self.file_path, 'r', encoding=encoding) as f:
                content = f.read()
        except UnicodeDecodeError:
            raise ValueError("Cannot perform text replacement on non-text / binary files.")

        if target not in content:
            return False

        new_content = content.replace(target, replacement, count)
        
        if new_content == content:
            return False

        with open(self.file_path, 'w', encoding=encoding) as f:
            f.write(new_content)
            
        return True

    def _write_content(self, content: Union[str, bytes], mode: str, encoding: str) -> bool:
        """Internal helper to write content"""
        if isinstance(content, str):
            with open(self.file_path, mode, encoding=encoding) as f:
                f.write(content)
        elif isinstance(content, bytes):
            # Binary mode requires 'b' in the mode string (e.g., 'wb', 'ab')
            bin_mode = mode + 'b'
            with open(self.file_path, bin_mode) as f:
                f.write(content)
        else:
            raise TypeError("Content must be str or bytes")
        
        return True

# Convenience functions
def create_file(file_path: Union[str, Path], content: Union[str, bytes] = "", overwrite: bool = False, encoding: str = 'utf-8') -> bool:
    """Create a file"""
    return FileWriter(file_path).create(content, overwrite, encoding)

def write_to_file(file_path: Union[str, Path], content: Union[str, bytes], encoding: str = 'utf-8') -> bool:
    """Overwrites file with content"""
    return FileWriter(file_path).write(content, encoding)

def append_to_file(file_path: Union[str, Path], content: Union[str, bytes], new_line: bool = False, encoding: str = 'utf-8') -> bool:
    """Appends content to file"""
    return FileWriter(file_path).append(content, new_line, encoding)

def replace_in_file(file_path: Union[str, Path], target: str, replacement: str, count: int = -1, encoding: str = 'utf-8') -> bool:
    """Replaces text in file"""
    return FileWriter(file_path).replace(target, replacement, count, encoding)

if __name__ == "__main__":
    import sys
    
    # Simple CLI for testing
    if len(sys.argv) < 3:
        print("Usage: python file_writer.py <action> <file_path> [content/target] [replacement]")
        print("Actions: create, write, append, replace")
        sys.exit(1)
        
    action = sys.argv[1]
    path = sys.argv[2]
    
    writer = FileWriter(path)
    
    try:
        if action == "create":
            content = sys.argv[3] if len(sys.argv) > 3 else ""
            writer.create(content)
            print(f"Created {path}")
            
        elif action == "write":
            content = sys.argv[3] if len(sys.argv) > 3 else ""
            writer.write(content)
            print(f"Wrote to {path}")
            
        elif action == "append":
            content = sys.argv[3] if len(sys.argv) > 3 else ""
            writer.append(content, new_line=True)
            print(f"Appended to {path}")
            
        elif action == "replace":
            if len(sys.argv) < 5:
                print("Error: replace requires target and replacement strings")
                sys.exit(1)
            target = sys.argv[3]
            replacement = sys.argv[4]
            if writer.replace(target, replacement):
                print(f"Replaced '{target}' with '{replacement}' in {path}")
            else:
                print(f"Target '{target}' not found in {path}")
        else:
            print(f"Unknown action: {action}")
            
    except Exception as e:
        print(f"Error: {e}")
