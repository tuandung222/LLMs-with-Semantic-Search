"""
Script to generate and cache embeddings for sample data.
This script should be run before starting the API server to ensure embeddings are cached.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.semantic_search.generate_embeddings import EmbeddingGenerator

def main():
    """Generate and cache embeddings for sample data."""
    print("\nStarting embedding generation...")
    print("=" * 50)
    
    try:
        generator = EmbeddingGenerator()
        generator.generate_and_cache_embeddings()
        print("\nEmbedding generation completed successfully!")
        
    except Exception as e:
        print(f"\nError generating embeddings: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 