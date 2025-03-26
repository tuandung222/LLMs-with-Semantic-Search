import os
from dotenv import load_dotenv
import weaviate
import openai
from semantic_search.embedding_manager import EmbeddingManager
from semantic_search.config import (
    OPENAI_API_KEY,
    WEAVIATE_URL,
    WEAVIATE_API_KEY,
)

def test_openai_connection():
    """Test OpenAI API connection."""
    try:
        # Initialize client correctly for version 1.12.0
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="Test connection",
            encoding_format="float"
        )
        print("✅ OpenAI API connection successful!")
        print(f"Embedding dimension: {len(response.data[0].embedding)}")
        return True
    except Exception as e:
        print("❌ OpenAI API connection failed!")
        print(f"Error: {str(e)}")
        return False

def test_weaviate_connection():
    """Test Weaviate connection."""
    try:
        # For local deployment without authentication
        client = weaviate.Client(
            url=WEAVIATE_URL,
            additional_headers={
                "X-OpenAI-Api-Key": OPENAI_API_KEY,
            }
        )
        
        # Check if Weaviate is ready
        is_ready = client.is_ready()
        if is_ready:
            print("✅ Weaviate connection successful!")
            
            # Check if Articles class exists
            schema = client.schema.get()
            classes = [c["class"] for c in schema["classes"]]
            if "Articles" in classes:
                print("✅ Articles class found in Weaviate!")
                return True
            else:
                print("❌ Articles class not found in Weaviate!")
                return False
        else:
            print("❌ Weaviate is not ready!")
            return False
    except Exception as e:
        print("❌ Weaviate connection failed!")
        print(f"Error: {str(e)}")
        return False

def test_semantic_search():
    """Test semantic search functionality."""
    try:
        embedding_manager = EmbeddingManager()
        query = "What is artificial intelligence?"
        texts, similarities = embedding_manager.search(query, num_results=3)
        
        print("\n✅ Semantic search successful!")
        print(f"\nQuery: {query}")
        print("\nResults:")
        for i, (text, similarity) in enumerate(zip(texts, similarities), 1):
            print(f"\n{i}. Similarity: {similarity:.4f}")
            print(f"Text: {text[:200]}...")
        return True
    except Exception as e:
        print("❌ Semantic search failed!")
        print(f"Error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🔍 Testing API and App Connections...\n")
    
    # Load environment variables
    load_dotenv()
    
    # Run tests
    openai_success = test_openai_connection()
    weaviate_success = test_weaviate_connection()
    search_success = test_semantic_search()
    
    # Print summary
    print("\n📊 Test Summary:")
    print(f"OpenAI API: {'✅' if openai_success else '❌'}")
    print(f"Weaviate: {'✅' if weaviate_success else '❌'}")
    print(f"Semantic Search: {'✅' if search_success else '❌'}")

if __name__ == "__main__":
    main() 