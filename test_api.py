import unittest
import requests
from typing import Dict, Any

class TestAPICompatibility(unittest.TestCase):
    """Test suite to verify API response format compatibility between server and demo app."""
    
    def setUp(self):
        """Set up test case with API endpoint."""
        self.base_url = "http://localhost:8000"
        
    def test_ask_question_response_format(self):
        """Test if /ask-question endpoint returns response in the format expected by demo app."""
        # Test data
        question_data = {
            "question": "What is artificial intelligence?",
            "num_search_results": 3,
            "num_generations": 1
        }
        
        # Make request to API
        response = requests.post(f"{self.base_url}/ask-question", json=question_data)
        self.assertEqual(response.status_code, 200, "API request failed")
        
        # Get response data
        data = response.json()
        
        # Test response structure
        self.assertIn("answers", data, "Response missing 'answers' field")
        self.assertIn("documents", data, "Response missing 'documents' field")
        self.assertIn("relevance_scores", data, "Response missing 'relevance_scores' field")
        
        # Test data types
        self.assertIsInstance(data["answers"], list, "'answers' should be a list")
        self.assertIsInstance(data["documents"], list, "'documents' should be a list")
        self.assertIsInstance(data["relevance_scores"], list, "'relevance_scores' should be a list")
        
        # Test list lengths match
        self.assertEqual(len(data["documents"]), len(data["relevance_scores"]), 
                        "Number of documents should match number of relevance scores")
        
        # Test data content
        if len(data["answers"]) > 0:
            self.assertIsInstance(data["answers"][0], str, "Answer should be a string")
        if len(data["documents"]) > 0:
            self.assertIsInstance(data["documents"][0], str, "Document should be a string")
        if len(data["relevance_scores"]) > 0:
            self.assertIsInstance(data["relevance_scores"][0], float, "Relevance score should be a float")
            
    def test_search_response_format(self):
        """Test if /search endpoint returns response in the format expected by demo app."""
        # Test data
        search_data = {
            "query": "artificial intelligence",
            "num_results": 3
        }
        
        # Make request to API
        response = requests.post(f"{self.base_url}/search", json=search_data)
        self.assertEqual(response.status_code, 200, "API request failed")
        
        # Get response data
        data = response.json()
        
        # Test response structure
        self.assertIsInstance(data, dict, "Response should be a dictionary")
        self.assertIn("results", data, "Response missing 'results' field")
        
        # Test results field
        results = data["results"]
        self.assertIsInstance(results, list, "'results' should be a list")
        if len(results) > 0:
            self.assertIsInstance(results[0], str, "Search result should be a string")
        
        # Test optional distances field
        if "distances" in data:
            distances = data["distances"]
            self.assertIsInstance(distances, list, "'distances' should be a list")
            self.assertEqual(len(results), len(distances), 
                           "Number of results should match number of distances")
            if len(distances) > 0:
                self.assertIsInstance(distances[0], float, "Distance should be a float")

if __name__ == "__main__":
    unittest.main() 