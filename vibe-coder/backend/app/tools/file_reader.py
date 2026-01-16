"""
Universal File Reader Utility

This module provides functionality to read various file types including:
- Text files (.txt, .md, .csv, .json, .xml, .html, .css, .js, .py, etc.)
- Binary files (.pdf, .docx, .xlsx, etc.)
- Image files (.jpg, .png, .gif, .bmp, etc.)
- Audio/Video files (metadata extraction)
"""

import os
import mimetypes
from pathlib import Path
from typing import Union, Dict, Any, Optional
import base64


class FileReader:
    """Universal file reader that handles multiple file types"""
    
    # Text file extensions
    TEXT_EXTENSIONS = {
        '.txt', '.md', '.csv', '.json', '.xml', '.html', '.htm', 
        '.css', '.js', '.py', '.java', '.cpp', '.c', '.h', '.hpp',
        '.sh', '.bash', '.yaml', '.yml', '.toml', '.ini', '.conf',
        '.log', '.sql', '.r', '.rb', '.go', '.rs', '.swift', '.kt',
        '.ts', '.tsx', '.jsx', '.vue', '.php', '.pl', '.lua'
    }
    
    # Binary file extensions
    BINARY_EXTENSIONS = {
        '.pdf', '.docx', '.xlsx', '.pptx', '.zip', '.tar', '.gz',
        '.rar', '.7z', '.exe', '.dll', '.so', '.dylib'
    }
    
    # Image file extensions
    IMAGE_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico',
        '.webp', '.tiff', '.tif', '.psd', '.raw'
    }
    
    # Audio/Video file extensions
    MEDIA_EXTENSIONS = {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma',
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'
    }
    
    def __init__(self, file_path: Union[str, Path]):
        """
        Initialize the FileReader with a file path
        
        Args:
            file_path: Path to the file to read
        """
        self.file_path = Path(file_path)
        self.extension = self.file_path.suffix.lower()
        self.mime_type = mimetypes.guess_type(str(self.file_path))[0]
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
    
    def read(self, encoding: str = 'utf-8', errors: str = 'ignore') -> Dict[str, Any]:
        """
        Read the file and return its contents with metadata
        
        Args:
            encoding: Text encoding to use (default: utf-8)
            errors: How to handle encoding errors (default: ignore)
            
        Returns:
            Dictionary containing file metadata and content
        """
        file_info = self._get_file_info()
        
        if self._is_text_file():
            content = self._read_text(encoding, errors)
            file_info['content_type'] = 'text'
            file_info['content'] = content
        elif self._is_image_file():
            content = self._read_binary()
            file_info['content_type'] = 'image'
            file_info['content'] = content
            file_info['base64'] = base64.b64encode(content).decode('utf-8')
        elif self._is_media_file():
            file_info['content_type'] = 'media'
            file_info['content'] = None
            file_info['message'] = 'Media file detected. Use specialized libraries for processing.'
        else:
            content = self._read_binary()
            file_info['content_type'] = 'binary'
            file_info['content'] = content
            file_info['base64'] = base64.b64encode(content).decode('utf-8')
        
        return file_info
    
    def read_text(self, encoding: str = 'utf-8', errors: str = 'ignore') -> str:
        """
        Read file as text
        
        Args:
            encoding: Text encoding to use
            errors: How to handle encoding errors
            
        Returns:
            File content as string
        """
        return self._read_text(encoding, errors)
    
    def read_binary(self) -> bytes:
        """
        Read file as binary
        
        Returns:
            File content as bytes
        """
        return self._read_binary()
    
    def read_lines(self, encoding: str = 'utf-8', errors: str = 'ignore') -> list:
        """
        Read file as list of lines
        
        Args:
            encoding: Text encoding to use
            errors: How to handle encoding errors
            
        Returns:
            List of lines
        """
        with open(self.file_path, 'r', encoding=encoding, errors=errors) as f:
            return f.readlines()
    
    def read_base64(self) -> str:
        """
        Read file and encode as base64 string
        
        Returns:
            Base64 encoded string
        """
        content = self._read_binary()
        return base64.b64encode(content).decode('utf-8')
    
    def _read_text(self, encoding: str = 'utf-8', errors: str = 'ignore') -> str:
        """Read file as text"""
        with open(self.file_path, 'r', encoding=encoding, errors=errors) as f:
            return f.read()
    
    def _read_binary(self) -> bytes:
        """Read file as binary"""
        with open(self.file_path, 'rb') as f:
            return f.read()
    
    def _is_text_file(self) -> bool:
        """Check if file is a text file"""
        if self.extension in self.TEXT_EXTENSIONS:
            return True
        if self.mime_type and self.mime_type.startswith('text/'):
            return True
        return False
    
    def _is_image_file(self) -> bool:
        """Check if file is an image file"""
        if self.extension in self.IMAGE_EXTENSIONS:
            return True
        if self.mime_type and self.mime_type.startswith('image/'):
            return True
        return False
    
    def _is_media_file(self) -> bool:
        """Check if file is a media file"""
        if self.extension in self.MEDIA_EXTENSIONS:
            return True
        if self.mime_type and (self.mime_type.startswith('audio/') or 
                               self.mime_type.startswith('video/')):
            return True
        return False
    
    def _get_file_info(self) -> Dict[str, Any]:
        """Get file metadata"""
        stat = self.file_path.stat()
        return {
            'filename': self.file_path.name,
            'path': str(self.file_path.absolute()),
            'extension': self.extension,
            'mime_type': self.mime_type,
            'size_bytes': stat.st_size,
            'size_kb': round(stat.st_size / 1024, 2),
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
        }


# Convenience functions
def read_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    Read any file and return its contents with metadata
    
    Args:
        file_path: Path to the file
        encoding: Text encoding (default: utf-8)
        
    Returns:
        Dictionary with file info and content
    """
    reader = FileReader(file_path)
    return reader.read(encoding=encoding)


def read_text_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """
    Read a text file
    
    Args:
        file_path: Path to the file
        encoding: Text encoding (default: utf-8)
        
    Returns:
        File content as string
    """
    reader = FileReader(file_path)
    return reader.read_text(encoding=encoding)


def read_binary_file(file_path: Union[str, Path]) -> bytes:
    """
    Read a binary file
    
    Args:
        file_path: Path to the file
        
    Returns:
        File content as bytes
    """
    reader = FileReader(file_path)
    return reader.read_binary()


def read_file_base64(file_path: Union[str, Path]) -> str:
    """
    Read a file and encode as base64
    
    Args:
        file_path: Path to the file
        
    Returns:
        Base64 encoded string
    """
    reader = FileReader(file_path)
    return reader.read_base64()


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python file_reader.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        result = read_file(file_path)
        print(f"File: {result['filename']}")
        print(f"Type: {result['content_type']}")
        print(f"Size: {result['size_kb']} KB")
        print(f"MIME: {result['mime_type']}")
        print("\nContent preview:")
        
        if result['content_type'] == 'text':
            content = result['content']
            print(content[:500] + ('...' if len(content) > 500 else ''))
        elif result['content_type'] in ['image', 'binary']:
            print(f"Binary data ({len(result['content'])} bytes)")
            print(f"Base64: {result['base64'][:100]}...")
        else:
            print(result.get('message', 'No content available'))
            
    except Exception as e:
        print(f"Error reading file: {e}")
