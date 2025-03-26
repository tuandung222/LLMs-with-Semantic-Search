from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from semantic_search.search_interface import SemanticSearchInterface
from semantic_search.config import SearchConfig
from semantic_search.sample_data import get_all_sample_data

app = FastAPI(
    title="Search Server API",
    description="API for semantic search and question answering",
    version="1.0.0"
)

# Initialize the search interface with sample data loading enabled by default
load_sample_data = os.getenv("LOAD_SAMPLE_DATA", "true").lower() == "true"
search_interface = SemanticSearchInterface(load_sample_data=load_sample_data)

class SearchRequest(BaseModel):
    query: str
    num_results: int = 3

class QuestionRequest(BaseModel):
    question: str
    num_search_results: int = 3
    num_generations: int = 1

class TextRequest(BaseModel):
    text: str

@app.post("/process-text")
def process_text(request: TextRequest):
    """Process and index new text."""
    try:
        search_interface.process_and_index_text(request.text)
        return {"message": "Text processed successfully"}
    except Exception as e:
        error_msg = str(e)
        print(f"Error processing text: {error_msg}")
        if "API key" in error_msg or "authentication" in error_msg.lower():
            raise HTTPException(status_code=401, detail="Authentication error with OpenAI API. Please check your API key.")
        elif "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
            raise HTTPException(status_code=429, detail="Rate limit exceeded with OpenAI API.")
        else:
            raise HTTPException(status_code=500, detail=f"Internal server error: {error_msg}")

@app.post("/search")
def search(request: SearchRequest) -> Dict[str, Any]:
    """Perform semantic search."""
    try:
        response = search_interface.search(request.query, request.num_results)
        # Return results in the format expected by the demo app
        return {
            "results": response["results"],
            "distances": response.get("distances", [])
        }
    except Exception as e:
        error_msg = str(e)
        print(f"Error in search endpoint: {error_msg}")
        if "API key" in error_msg or "authentication" in error_msg.lower():
            raise HTTPException(status_code=401, detail="Authentication error with OpenAI API. Please check your API key.")
        elif "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
            raise HTTPException(status_code=429, detail="Rate limit exceeded with OpenAI API.")
        else:
            raise HTTPException(status_code=500, detail=f"Search error: {error_msg}")

@app.post("/ask-question")
def ask_question(request: QuestionRequest) -> Dict[str, Any]:
    """Ask a question and get an answer."""
    try:
        response = search_interface.ask_question(
            request.question,
            request.num_search_results,
            request.num_generations
        )
        return response  # The response is already in the correct format
    except Exception as e:
        error_msg = str(e)
        print(f"Error in ask-question endpoint: {error_msg}")
        if "API key" in error_msg or "authentication" in error_msg.lower():
            raise HTTPException(status_code=401, detail="Authentication error with OpenAI API. Please check your API key.")
        elif "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
            raise HTTPException(status_code=429, detail="Rate limit exceeded with OpenAI API.")
        else:
            raise HTTPException(status_code=500, detail=f"Question answering error: {error_msg}")

@app.post("/clear-database")
def clear_database():
    """Clear all data from the database."""
    try:
        search_interface.clear_database()
        return {"message": "Database cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
@app.head("/health")  # Add support for HEAD requests which Docker's healthcheck uses
def health_check():
    """Health check endpoint."""
    status = "healthy"
    message = "Service is running"
    
    # Don't throw exceptions that could affect the status code
    try:
        # Lightweight schema check
        search_interface.embedding_manager.client.schema.get()
        message += " and connected to database"
    except Exception as e:
        status = "degraded"
        message += " but database connection has issues"
        print(f"Health check warning: {str(e)}")
    
    # Always return 200 OK to pass Docker's healthcheck
    return {"status": status, "message": message}

@app.get("/database-contents")
def get_database_contents() -> List[str]:
    """Get all contents from the database."""
    try:
        return search_interface.get_database_contents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sample-queries")
def get_sample_queries() -> List[str]:
    """Get sample queries for testing."""
    return [
        "What are the benefits of cloud computing?",
        "How does 5G technology improve network performance?",
        "What are the main cybersecurity threats today?",
        "How does blockchain technology work?",
        "What are the key principles of quantum physics?",
        "How does climate change affect our environment?",
        "What is the structure of DNA?",
        "What are the latest developments in space exploration?",
        "How has digital marketing evolved?",
        "What are the advantages of remote work?"
    ] 