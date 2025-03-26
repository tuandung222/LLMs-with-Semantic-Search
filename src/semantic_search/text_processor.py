from typing import List
import numpy as np
from .config import CHUNK_SEPARATOR, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP

class TextProcessor:
    """Handles text processing operations like chunking and cleaning."""
    
    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
    ):
        """
        Initialize the text processor.
        
        Args:
            chunk_size: Size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_into_paragraphs(self, text: str) -> List[str]:
        """
        Split text into paragraphs.
        
        Args:
            text: Input text to split
            
        Returns:
            List of paragraphs
        """
        paragraphs = text.split(CHUNK_SEPARATOR)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            
            if end > text_length:
                chunks.append(text[start:])
                break
                
            # Find the last space before chunk_size
            last_space = text.rfind(' ', start, end)
            if last_space != -1:
                end = last_space
                
            chunks.append(text[start:end])
            start = end - self.chunk_overlap
            
        return chunks
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace and normalizing line endings.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Normalize line endings
        text = text.replace('\r\n', '\n')
        return text.strip()
    
    def process_text(self, text: str) -> np.ndarray:
        """
        Process text by cleaning and splitting into chunks.
        
        Args:
            text: Input text to process
            
        Returns:
            Numpy array of processed text chunks
        """
        cleaned_text = self.clean_text(text)
        chunks = self.chunk_text(cleaned_text)
        return np.array(chunks) 