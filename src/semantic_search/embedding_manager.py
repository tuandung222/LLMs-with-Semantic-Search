import openai
import os
import weaviate
from typing import List, Tuple, Optional
from .config import (
    OPENAI_API_KEY,
    WEAVIATE_URL,
    WEAVIATE_API_KEY,
    OPENAI_EMBEDDING_MODEL,
)

# Import weaviate after other imports to avoid circular imports

class EmbeddingManager:
    """Manages text embeddings and similarity search operations using Weaviate."""
    
    def __init__(self):
        """Initialize the embedding manager with OpenAI and Weaviate clients."""
        # Debug environment variables
        print(f"Initializing EmbeddingManager with:")
        print(f"OPENAI_API_KEY present: {bool(OPENAI_API_KEY)}")
        print(f"WEAVIATE_URL: {os.getenv('WEAVIATE_URL', 'not set')}")
        
        try:
            # Initialize Weaviate client with authentication
            weaviate_url = os.getenv("WEAVIATE_URL", "http://weaviate:8080")
            self.client = weaviate.Client(
                url=weaviate_url,
                auth_client_secret=None,
                additional_headers={
                    "X-OpenAI-Api-Key": OPENAI_API_KEY  # Use the config value instead of getting from env again
                }
            )
            print(f"Successfully connected to Weaviate at {weaviate_url}")
        except Exception as e:
            print(f"Error connecting to Weaviate: {str(e)}")
            print(f"Creating a dummy client for development")
            self.client = None
        
    def get_embedding(self, text: str) -> List[float]:
        """
        Create embedding for a single text using OpenAI.
        
        Args:
            text: Text string to embed
            
        Returns:
            Embedding as list of floats
        """
        try:
            # Use the older 0.28.0 OpenAI API style
            openai.api_key = OPENAI_API_KEY
            
            # Call the embeddings API directly from the module
            response = openai.Embedding.create(
                model=OPENAI_EMBEDDING_MODEL,
                input=text
            )
            return response["data"][0]["embedding"]
        except Exception as e:
            print(f"OpenAI embedding error in get_embedding: {str(e)}")
            # Return dummy embedding with correct dimension
            # text-embedding-3-small produces 1536-dimensional vectors
            return [0.0] * 1536
    
    def search(
        self,
        query: str,
        num_results: int = 5,
        include_distances: bool = True
    ) -> Tuple[List[str], Optional[List[float]]]:
        """
        Search for similar texts using Weaviate's vector similarity search.
        
        Args:
            query: Search query
            num_results: Number of results to return
            include_distances: Whether to include distances in results
            
        Returns:
            Tuple of (list of texts, optional list of similarity scores)
        """
        try:
            # Get query embedding
            query_embedding = self.get_embedding(query)
            
            # Perform vector similarity search in Weaviate
            result = (
                self.client.query
                .get("Articles", ["text"])
                .with_near_vector({
                    "vector": query_embedding
                })
                .with_limit(num_results)
                .with_additional(["distance"] if include_distances else [])
                .do()
            )
            
            # Extract results, handle case when no results are found
            if (not result.get("data") or 
                not result["data"].get("Get") or 
                not result["data"]["Get"].get("Articles") or 
                len(result["data"]["Get"]["Articles"]) == 0):
                print("No search results found in the database")
                return [], [] if include_distances else None
                
            articles = result["data"]["Get"]["Articles"]
            texts = [article.get("text", "") for article in articles]
            
            # Return distances if requested
            if include_distances:
                # Convert distances to similarities (1 - distance)
                similarities = []
                for article in articles:
                    if "_additional" in article and "distance" in article["_additional"]:
                        similarities.append(1 - article["_additional"]["distance"])
                    else:
                        similarities.append(0.0)  # Default similarity if distance is missing
                return texts, similarities
            
            return texts, None
        except Exception as e:
            print(f"Error in search: {str(e)}")
            # Return empty results instead of failing
            return [], [] if include_distances else None

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts using OpenAI.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embeddings as lists of floats
        """
        # Process texts in batches to avoid rate limits
        embeddings = []
        batch_size = 100  # OpenAI allows up to 2048 texts per request, but we'll be conservative
        
        try:
            # Set API key for the older style API
            openai.api_key = OPENAI_API_KEY
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                try:
                    response = openai.Embedding.create(
                        model=OPENAI_EMBEDDING_MODEL,
                        input=batch
                    )
                    batch_embeddings = [item["embedding"] for item in response["data"]]
                    embeddings.extend(batch_embeddings)
                except Exception as e:
                    print(f"OpenAI embedding error for batch {i//batch_size}: {str(e)}")
                    # Fall back to dummy embeddings with correct dimension for this model
                    # text-embedding-3-small produces 1536-dimensional vectors
                    dimension = 1536
                    dummy_embeddings = [[0.0] * dimension for _ in range(len(batch))]
                    print(f"Using dummy embeddings for this batch")
                    embeddings.extend(dummy_embeddings)
            
            return embeddings
        except Exception as e:
            print(f"Fatal error in create_embeddings: {str(e)}")
            # Return dummy embeddings for the requested number of texts
            dimension = 1536
            return [[0.0] * dimension for _ in range(len(texts))]

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Alias for create_embeddings for backward compatibility."""
        return self.create_embeddings(texts)

    def build_search_index(self, texts: List[str], embeddings: List[List[float]]):
        """
        Build search index in Weaviate using text chunks and their embeddings.
        Checks for duplicates before adding new documents.
        
        Args:
            texts: List of text chunks
            embeddings: List of embeddings corresponding to the text chunks
        """
        # Check if client is None (development or error mode)
        if self.client is None:
            print("Warning: Weaviate client is not available, skipping index building")
            return

        # Ensure the schema exists
        self._ensure_schema_exists()
        
        # Add data objects with vectors
        with self.client.batch as batch:
            batch.batch_size = 100
            for text, embedding in zip(texts, embeddings):
                # Check if text already exists
                result = (
                    self.client.query
                    .get("Articles", ["text"])
                    .with_where({
                        "path": ["text"],
                        "operator": "Equal",
                        "valueText": text
                    })
                    .do()
                )
                
                # Only add if text doesn't exist
                if not result["data"]["Get"]["Articles"]:
                    # Create data object
                    properties = {
                        "text": text,
                    }
                    
                    # Add the object with its vector
                    batch.add_data_object(
                        data_object=properties,
                        class_name="Articles",
                        vector=embedding
                    )

    def clear_database(self):
        """Clear all contents from the database."""
        # Check if client is None (development or error mode)
        if self.client is None:
            print("Warning: Weaviate client is not available, skipping database clearing")
            return
            
        try:
            print("Clearing existing database...")
            # Ensure schema exists before attempting to delete
            self._ensure_schema_exists()
            
            # Delete all objects in the Articles class where text exists
            self.client.batch.delete_objects(
                class_name="Articles",
                where={
                    "path": ["text"],
                    "operator": "Like",
                    "valueString": "*"  # Match any text
                }
            )
            print("Database cleared successfully")
        except Exception as e:
            print(f"Error clearing database: {str(e)}")
            raise e

    def _ensure_schema_exists(self):
        """Ensure the required Weaviate schema exists."""
        # Check if client is None (development or error mode)
        if self.client is None:
            print("Warning: Weaviate client is not available, skipping schema check")
            return
            
        try:
            # Check if schema exists
            schema = self.client.schema.get()
            classes = [c["class"] for c in schema["classes"]] if schema.get("classes") else []
            
            if "Articles" not in classes:
                # Define the schema
                class_obj = {
                    "class": "Articles",
                    "vectorizer": "none",  # We provide vectors manually
                    "properties": [
                        {
                            "name": "text",
                            "dataType": ["text"],
                            "description": "The text content",
                        }
                    ]
                }
                
                # Create the schema
                self.client.schema.create_class(class_obj)
                
        except Exception as e:
            raise Exception(f"Failed to ensure schema exists: {str(e)}")

    def get_all_texts(self, limit: int = 100) -> List[str]:
        """
        Get all texts stored in the database up to the specified limit.
        
        Args:
            limit: Maximum number of texts to return
            
        Returns:
            List of texts from the database
        """
        # Check if client is None (development or error mode)
        if self.client is None:
            print("Warning: Weaviate client is not available, returning empty list")
            return []
            
        result = (
            self.client.query
            .get("Articles", ["text"])
            .with_limit(limit)
            .do()
        )
        
        if result and "data" in result and "Get" in result["data"] and "Articles" in result["data"]["Get"]:
            articles = result["data"]["Get"]["Articles"]
            return [article["text"] for article in articles if "text" in article]
        return [] 
