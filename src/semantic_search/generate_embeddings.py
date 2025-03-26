import os
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from .embedding_manager import EmbeddingManager
from .text_processor import TextProcessor
from .sample_data import get_all_sample_data
from .config import CACHE_DIR

class EmbeddingGenerator:
    def __init__(self):
        self.embedding_manager = EmbeddingManager()
        self.text_processor = TextProcessor()
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_and_cache_embeddings(self):
        """Generate embeddings for all sample data and cache them."""
        print("Generating embeddings for sample data...")
        
        # Get all sample data
        samples = get_all_sample_data()
        
        # Process each sample
        cached_data = []
        for sample in samples:
            print(f"Processing: {sample['title']}")
            
            # Process text into chunks
            chunks = self.text_processor.process_text(sample['text'])
            
            # Generate embeddings
            embeddings = self.embedding_manager.get_embeddings(chunks)
            
            # Convert numpy arrays to lists if needed
            chunks_list = chunks.tolist() if isinstance(chunks, np.ndarray) else chunks
            embeddings_list = [emb.tolist() if isinstance(emb, np.ndarray) else emb for emb in embeddings]
            
            # Create cache entry
            cache_entry = {
                'title': sample['title'],
                'field': sample['field'],
                'text': sample['text'],
                'chunks': chunks_list,
                'embeddings': embeddings_list
            }
            cached_data.append(cache_entry)
        
        # Save to cache file
        cache_file = self.cache_dir / 'sample_embeddings.json'
        with open(cache_file, 'w') as f:
            json.dump(cached_data, f, indent=2)
        
        print(f"\nEmbeddings cached successfully at: {cache_file}")
        print(f"Total samples processed: {len(samples)}")
        
    def load_cached_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Load cached embeddings for the given texts if they exist.
        
        Args:
            texts: List of texts to get embeddings for
            
        Returns:
            List of embeddings if found in cache, None otherwise
        """
        try:
            # Create a unique filename based on the content
            text_string = ''.join([str(t) for t in texts])
            cache_key = hash(text_string)
            cache_file = self.cache_dir / f"embeddings_{cache_key}.npy"
            
            if cache_file.exists():
                print("Loading cached embeddings...")
                return np.load(str(cache_file)).tolist()
            return None
        except Exception as e:
            print(f"Error loading cached embeddings: {str(e)}")
            return None
            
    def cache_embeddings(self, texts: List[str], embeddings: List[List[float]]) -> None:
        """
        Cache embeddings for the given texts.
        
        Args:
            texts: List of texts that were embedded
            embeddings: List of embeddings to cache
        """
        try:
            # Create a unique filename based on the content
            text_string = ''.join([str(t) for t in texts])
            cache_key = hash(text_string)
            cache_file = self.cache_dir / f"embeddings_{cache_key}.npy"
            
            # Save embeddings to cache
            np.save(str(cache_file), np.array(embeddings))
            print("Embeddings cached successfully")
        except Exception as e:
            print(f"Error caching embeddings: {str(e)}")

def main():
    """Generate and cache embeddings for sample data."""
    generator = EmbeddingGenerator()
    generator.generate_and_cache_embeddings()

if __name__ == "__main__":
    main() 