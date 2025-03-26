import streamlit as st
import requests
from typing import List, Dict, Any
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get default API key from environment
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Get API URL from environment variable or use the Docker service name as default
API_URL = os.getenv("API_URL", "http://search_server:8000")

def check_server_health() -> bool:
    try:
        response = requests.get(f"{API_URL}/health")
        return response.status_code == 200
    except:
        return False

def get_database_contents() -> List[str]:
    try:
        response = requests.get(f"{API_URL}/database-contents")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def get_sample_queries() -> List[str]:
    try:
        response = requests.get(f"{API_URL}/sample-queries")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def process_text(text: str) -> None:
    """Add text to the database."""
    try:
        response = requests.post(
            f"{API_URL}/process-text",
            json={"text": text}
        )
        if response.status_code == 200:
            st.success("Text successfully added to database!")
        else:
            st.error("Failed to add text to database.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def clear_database() -> None:
    """Clear all contents from the database."""
    try:
        response = requests.post(f"{API_URL}/clear-database")
        if response.status_code == 200:
            st.success("Database cleared successfully!")
        else:
            st.error("Failed to clear database.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def search(query: str, num_results: int) -> Dict[str, Any]:
    response = requests.post(
        f"{API_URL}/search",
        json={"query": query, "num_results": num_results}
    )
    return response.json()

def ask_question(question: str, num_search_results: int, num_generations: int, api_key: str = None, model: str = "gpt-4-turbo-preview") -> Dict[str, Any]:
    """Send a question to the API and get the answer."""
    try:
        # Use provided API key or default from environment
        api_key = api_key or DEFAULT_OPENAI_API_KEY
        if not api_key:
            st.error("Please provide an OpenAI API key in the sidebar or set it in your environment variables.")
            return None
            
        # The backend API doesn't accept model or api_key parameters
        # Only send the parameters that the backend expects
        response = requests.post(
            f"{API_URL}/ask-question",
            json={
                "question": question,
                "num_search_results": num_search_results,
                "num_generations": num_generations
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error asking question: {str(e)}")
        return None

def display_search_results(results: Dict[str, Any]):
    if not results.get("results"):
        st.warning("No results found.")
        return
        
    for i, (text, distance) in enumerate(zip(results["results"], results.get("distances", [])), 1):
        with st.expander(f"Result {i} (Distance: {distance:.4f})", expanded=True):
            st.markdown(text)

def display_qa_results(qa_response):
    """Display question-answering results."""
    if not qa_response:
        st.error("No response received from the server.")
        return

    # Display the answer(s)
    st.subheader("Answer")
    if "answers" in qa_response and qa_response["answers"]:
        for i, answer in enumerate(qa_response["answers"]):
            if i > 0:
                st.markdown("---")
            st.write(answer)
    else:
        st.write("No answer available")

    # Display relevant documents if available
    if "documents" in qa_response and qa_response["documents"]:
        st.subheader("Relevant Documents")
        for i, (doc, score) in enumerate(zip(
            qa_response["documents"], 
            qa_response.get("relevance_scores", [None] * len(qa_response["documents"]))
        )):
            with st.expander(f"Document {i+1}", expanded=False):
                st.write(doc)
                if score is not None:
                    st.write(f"Relevance Score: {score:.4f}")

def main():
    st.set_page_config(
        page_title="Semantic Search Demo",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("Semantic Search with LLMs")
    
    # Sidebar for API key and model selection
    with st.sidebar:
        st.header("Settings")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Enter your OpenAI API key here. It will be used for embeddings and question answering."
        )
        
        # Model selection
        selected_model = st.selectbox(
            "Select Model",
            [
                "gpt-4-turbo-preview",
                "gpt-4",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-16k"
            ],
            help="Select the OpenAI model to use for question answering. GPT-4 models provide better answers but are more expensive."
        )
        
        st.markdown("---")
        st.markdown("### Model Information")
        st.markdown(f"Using model: **{selected_model}**")
        st.markdown("Embedding model: **text-embedding-3-small**")

    # Create tabs
    tab_search, tab_qa, tab_db_manage, tab_db_contents = st.tabs([
        "🔍 Semantic Search",
        "❓ Question Answering",
        "📝 Database Management",
        "📚 Database Contents"
    ])

    # Semantic Search Tab
    with tab_search:
        st.header("Semantic Search")
        search_query = st.text_input("Enter your search query:")
        num_results = st.slider(
            "Number of results to return:",
            min_value=1,
            max_value=10,
            value=3
        )
        
        if st.button("Search"):
            if search_query:
                results = search(search_query, num_results)
                display_search_results(results)
            else:
                st.warning("Please enter a search query.")

    # Question Answering Tab
    with tab_qa:
        st.header("Question Answering")
        
        # Example questions
        example_questions = get_sample_queries()
        selected_example = st.selectbox(
            "Choose an example question or write your own:",
            ["Write your own question..."] + example_questions
        )
        
        if selected_example == "Write your own question...":
            question = st.text_input("Enter your question:")
        else:
            question = selected_example
            st.text_input("Or write your own question:", value=question)
        
        num_search_results = st.slider(
            "Number of search results to use:",
            min_value=1,
            max_value=10,
            value=3
        )
        
        num_generations = st.slider(
            "Number of answer generations:",
            min_value=1,
            max_value=5,
            value=1
        )
        
        if st.button("Ask Question"):
            if question:
                response = ask_question(question, num_search_results, num_generations, api_key, selected_model)
                display_qa_results(response)
            else:
                st.warning("Please enter a question.")

    # Database Management Tab
    with tab_db_manage:
        st.header("Database Management")
        
        # Text input section
        st.subheader("Add Text to Database")
        text_input = st.text_area(
            "Enter text to add to the database:",
            height=200,
            help="Enter the text you want to add to the search database."
        )
        
        if st.button("Add Text"):
            if text_input:
                process_text(text_input)
            else:
                st.warning("Please enter some text to add.")
        
        # Database clearing section
        st.subheader("Clear Database")
        st.warning("⚠️ This will remove all documents from the database!")
        if st.button("Clear Database"):
            clear_database()

    # Database Contents Tab
    with tab_db_contents:
        st.header("Database Contents")
        
        if st.button("Refresh Contents"):
            contents = get_database_contents()
            if contents:
                for i, text in enumerate(contents, 1):
                    with st.expander(f"Document {i}", expanded=False):
                        st.markdown(text)
            else:
                st.info("The database is empty. Add some documents in the Database Management tab.")

if __name__ == "__main__":
    main()