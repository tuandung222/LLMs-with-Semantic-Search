import openai
from typing import List, Dict, Any
import os

from .config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
    OPENAI_MAX_TOKENS
)

class GenerativeSearch:
    """Combines semantic search with text generation for question answering."""
    
    def __init__(self, embedding_manager):
        """
        Initialize the generative search with OpenAI client and embedding manager.
        
        Args:
            embedding_manager: Instance of EmbeddingManager for vector operations
        """
        try:
            # Set the API key for the older OpenAI API style (v0.28.0)
            openai.api_key = OPENAI_API_KEY
            self.embedding_manager = embedding_manager
            print(f"OpenAI API key set successfully for generative search")
        except Exception as e:
            print(f"Error initializing OpenAI: {str(e)}")
            # Simple fallback - disable OpenAI completely
            self.embedding_manager = embedding_manager
            print(f"OpenAI initialization failed, will use fallback responses")

    def generate_answer(self, query: str, context: List[str]) -> str:
        """
        Generate an answer based on the query and context using OpenAI.
        
        Args:
            query: The user's question
            context: List of relevant text passages
            
        Returns:
            Generated answer as a string
        """
        # Prepare the prompt
        prompt = f"""Based on the following context, please answer the question. If the context doesn't contain enough information to answer the question, say so.

Context:
{' '.join(context)}

Question: {query}

Answer:"""

        # If the API key is not set, return a fallback response
        if not openai.api_key:
            return f"I'm unable to generate an answer because the OpenAI API key is not set. " + \
                   f"Please check your API key and network configuration. " + \
                   f"The relevant context I found was: {context[0][:100]}..." if context else "No relevant context found."

        try:
            # Generate response using OpenAI with the older API style
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=OPENAI_TEMPERATURE,
                max_tokens=OPENAI_MAX_TOKENS
            )
            
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error generating answer: {str(e)}")
            return f"I'm unable to generate an answer due to a technical issue: {str(e)}"

    def search_and_generate(
        self,
        question: str,
        num_search_results: int = 1,
        num_generations: int = 1
    ) -> Dict[str, Any]:
        """
        Search for relevant passages and generate answers.
        
        Args:
            question: The user's question
            num_search_results: Number of search results to use for context
            num_generations: Number of different answers to generate
            
        Returns:
            Dictionary containing generated answers and retrieved documents
        """
        try:
            # Search for relevant passages
            results, distances = self.embedding_manager.search(
                query=question,
                num_results=num_search_results,
                include_distances=True
            )
            
            # Generate multiple answers if requested
            answers = []
            for _ in range(num_generations):
                answer = self.generate_answer(question, results)
                answers.append(answer)
                
            return {
                "answers": answers,
                "documents": results,
                "relevance_scores": [1 - d for d in distances] if distances else None
            }
        except Exception as e:
            print(f"Error in search_and_generate: {str(e)}")
            return {
                "answers": [f"I encountered an error: {str(e)}"],
                "documents": [],
                "relevance_scores": None
            } 