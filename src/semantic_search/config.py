import os
from dotenv import load_dotenv, find_dotenv
from typing import List
from pathlib import Path

# Load environment variables
_ = load_dotenv(find_dotenv())

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Helper to read secrets
def read_secret(secret_name, env_name, default=None):
    # First check for secrets file
    secret_file = os.environ.get(f"{env_name}_FILE")
    if secret_file and os.path.exists(secret_file):
        try:
            with open(secret_file, 'r') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading secret from {secret_file}: {e}")
    
    # Fall back to environment variable
    return os.environ.get(env_name, default)

# OpenAI Configuration
OPENAI_API_KEY = read_secret("openai_api_key", "OPENAI_API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"  # Default model for generation
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"  # Model for embeddings
OPENAI_TEMPERATURE = 0.5
OPENAI_MAX_TOKENS = 70

# Weaviate Configuration
WEAVIATE_URL = os.environ.get("WEAVIATE_URL", "http://localhost:8082")
WEAVIATE_API_KEY = read_secret("weaviate_api_key", "WEAVIATE_API_KEY", "")

# Search Configuration
SEARCH_LIMIT = 5
SEARCH_CERTAINTY = 0.7

# Search Configuration
DEFAULT_LANGUAGE = "en"
DEFAULT_PROPERTIES = ["title", "url", "text"]
DEFAULT_NUM_RESULTS = 3
DEFAULT_NUM_TREES = 10  # For AnnoyIndex

# Available languages for search
AVAILABLE_LANGUAGES = ["en", "de", "fr", "es", "it", "ja", "ar", "zh", "ko", "hi"]

# Text Processing
CHUNK_SEPARATOR = "\n\n"
DEFAULT_CHUNK_SIZE = 1000  # characters per chunk
DEFAULT_CHUNK_OVERLAP = 200  # characters overlap between chunks

# File Paths
INDEX_FILE = CACHE_DIR / "search_index.ann"
TEXT_FILE = CACHE_DIR / "sample_text.txt"

class SearchConfig:
    """Configuration class for search parameters."""
    
    def __init__(
        self,
        language: str = DEFAULT_LANGUAGE,
        properties: List[str] = DEFAULT_PROPERTIES,
        num_results: int = DEFAULT_NUM_RESULTS
    ):
        """
        Initialize search configuration.
        
        Args:
            language: Language code for search results
            properties: List of properties to return
            num_results: Number of results to return
        """
        if language not in AVAILABLE_LANGUAGES:
            raise ValueError(f"Language {language} not supported. Available languages: {AVAILABLE_LANGUAGES}")
            
        self.language = language
        self.properties = properties
        self.num_results = num_results 