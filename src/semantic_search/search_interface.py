from typing import List, Optional, Dict, Any
from .config import SearchConfig
from .text_processor import TextProcessor
from .embedding_manager import EmbeddingManager
from .generative_search import GenerativeSearch
from .sample_data import get_all_sample_data
from .generate_embeddings import EmbeddingGenerator

class SemanticSearchInterface:
    """Main interface for semantic search and question answering."""
    
    def __init__(
        self,
        search_config: Optional[SearchConfig] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        load_sample_data: bool = False,
        use_cached_embeddings: bool = True
    ):
        """
        Initialize the search interface.
        
        Args:
            search_config: Configuration for the search interface
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks
            load_sample_data: Whether to load sample data on initialization
            use_cached_embeddings: Whether to use cached embeddings
        """
        self.search_config = search_config or SearchConfig()
        self.text_processor = TextProcessor(chunk_size, chunk_overlap)
        self.embedding_manager = EmbeddingManager()
        self.embedding_generator = EmbeddingGenerator()
        self.generative_search = GenerativeSearch(embedding_manager=self.embedding_manager)
        
        # Clear existing data and load samples if requested
        self.clear_database()
        if load_sample_data:
            self._load_sample_data(use_cached_embeddings)
            
    def _load_sample_data(self, use_cached: bool = True):
        """
        Clear database and load sample texts into the vector database.
        If cached embeddings are available and use_cached is True, use them.
        Otherwise, generate new embeddings.
        
        Args:
            use_cached: Whether to use cached embeddings if available
        """
        print("Clearing existing database...")
        self.embedding_manager.clear_database()
        
        print("Loading sample data...")
        sample_data = get_all_sample_data()
        
        for article in sample_data:
            text = article["text"]
            title = article["title"]
            
            # Process text into chunks
            chunks = self.text_processor.process_text(text)
            
            # Try to get cached embeddings if enabled
            embeddings = None
            if use_cached:
                try:
                    embeddings = self.embedding_generator.load_cached_embeddings(chunks)
                    print(f"Using cached embeddings for: {title}")
                except:
                    print(f"No cached embeddings found for: {title}")
            
            # Generate new embeddings if needed
            if embeddings is None:
                print(f"Generating new embeddings for: {title}")
                embeddings = self.embedding_manager.create_embeddings(chunks.tolist())
                if use_cached:
                    self.embedding_generator.cache_embeddings(chunks, embeddings)
            
            # Add to database
            print(f"Adding article to database: {title}")
            self.embedding_manager.build_search_index(chunks, embeddings)
            
        print("Sample data loading complete")
        
    def process_and_index_text(self, text: str):
        """
        Process text and build search index.
        
        Args:
            text: Text to process and index
        """
        try:
            # Process text into chunks
            print("Step 1: Processing text into chunks")
            chunks = self.text_processor.process_text(text)
            
            # Create embeddings
            print(f"Step 2: Creating embeddings for {len(chunks)} text chunks")
            try:
                embeddings = self.embedding_manager.create_embeddings(chunks.tolist())
            except Exception as embedding_error:
                print(f"Error during embedding creation: {str(embedding_error)}")
                import traceback
                traceback.print_exc()
                raise Exception(f"Failed to create embeddings: {str(embedding_error)}")
            
            # Build search index
            print(f"Step 3: Building search index")
            self.embedding_manager.build_search_index(chunks, embeddings)
            
            print(f"Successfully processed and indexed text")
            return True
        except Exception as e:
            print(f"Error in process_and_index_text: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to process and index text: {str(e)}")
        
    def get_database_contents(self, limit: int = 100) -> List[str]:
        """
        Get the first N texts stored in the database.
        
        Args:
            limit: Maximum number of texts to return
            
        Returns:
            List of texts from the database
        """
        return self.embedding_manager.get_all_texts(limit)
        
    def save_index(self, filepath: str):
        """Save the search index to disk."""
        self.embedding_manager.save_index(filepath)
        
    def load_index(self, filepath: str):
        """Load the search index from disk."""
        self.embedding_manager.load_index(filepath)
        
    def clear_database(self):
        """Clear all contents from the vector database."""
        self.embedding_manager.clear_database()
        
    def search(
        self,
        query: str,
        num_results: Optional[int] = None,
        include_distances: bool = True
    ) -> Dict[str, Any]:
        """
        Perform semantic search.
        
        Args:
            query: Search query
            num_results: Number of results to return
            include_distances: Whether to include distances in results
            
        Returns:
            Dictionary containing search results and optionally distances
        """
        num_results = num_results or self.search_config.num_results
        results, distances = self.embedding_manager.search(
            query,
            num_results=num_results,
            include_distances=include_distances
        )
        
        response = {"results": results}
        if distances is not None:
            response["distances"] = distances
            
        return response
    
    def ask_question(
        self,
        question: str,
        num_search_results: int = 1,
        num_generations: int = 1
    ) -> Dict[str, Any]:
        """
        Ask a question and get generated answers.
        
        Args:
            question: The question to answer
            num_search_results: Number of search results to use for context
            num_generations: Number of different answers to generate
            
        Returns:
            Dictionary containing generated answers, source documents, and relevance scores
        """
        return self.generative_search.search_and_generate(
            question,
            num_search_results=num_search_results,
            num_generations=num_generations
        ) 