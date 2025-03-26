import os
from dotenv import load_dotenv
import weaviate
from semantic_search.config import (
    OPENAI_API_KEY,
    WEAVIATE_URL,
)
import openai

def setup_weaviate_schema():
    """Set up Weaviate schema for Articles class."""
    try:
        # Initialize the client
        client = weaviate.Client(
            url=WEAVIATE_URL,
            additional_headers={
                "X-OpenAI-Api-Key": OPENAI_API_KEY
            }
        )

        # Define the Articles class schema
        class_obj = {
            "class": "Articles",
            "description": "A collection of articles with embeddings for semantic search",
            "vectorizer": "none",  # Don't use a vectorizer, we'll provide vectors directly
            "properties": [
                {
                    "name": "title",
                    "dataType": ["text"],
                    "description": "The title of the article"
                },
                {
                    "name": "text",
                    "dataType": ["text"],
                    "description": "The main content of the article"
                },
                {
                    "name": "url",
                    "dataType": ["text"],
                    "description": "The URL of the article"
                }
            ]
        }

        # Check if class already exists
        schema = client.schema.get()
        existing_classes = [c["class"] for c in schema["classes"]] if schema.get("classes") else []

        if "Articles" in existing_classes:
            print("✅ Articles class already exists!")
            return True

        # Create the class
        client.schema.create_class(class_obj)
        print("✅ Successfully created Articles class!")

        # Initialize OpenAI client for embeddings
        openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Get embedding for sample article
        response = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input="Artificial Intelligence (AI) is revolutionizing how we live and work. From machine learning to neural networks, AI technologies are becoming increasingly sophisticated and capable of solving complex problems.",
            encoding_format="float"
        )
        vector = response.data[0].embedding

        # Add sample article
        sample_article = {
            "title": "Introduction to AI",
            "text": "Artificial Intelligence (AI) is revolutionizing how we live and work. From machine learning to neural networks, AI technologies are becoming increasingly sophisticated and capable of solving complex problems.",
            "url": "https://example.com/intro-to-ai"
        }

        # Add the article to Weaviate with its vector
        client.data_object.create(
            data_object=sample_article,
            class_name="Articles",
            vector=vector  # Provide the embedding vector directly
        )
        print("✅ Added sample article!")

        return True

    except Exception as e:
        print("❌ Failed to set up Weaviate schema!")
        print(f"Error: {str(e)}")
        return False

def main():
    """Run the setup."""
    print("🔧 Setting up Weaviate schema...\n")
    
    # Load environment variables
    load_dotenv()
    
    # Set up schema
    success = setup_weaviate_schema()
    
    # Print summary
    print("\n📊 Setup Summary:")
    print(f"Schema Setup: {'✅' if success else '❌'}")

if __name__ == "__main__":
    main() 