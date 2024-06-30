import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.routes import register_routes

class TestRoutes(unittest.TestCase):
    @patch('app.routes.load_models')
    @patch('app.routes.initialize_llm')
    def test_register_routes(self, mock_initialize_llm, mock_load_models):
        mock_get_embeddings = MagicMock()
        mock_get_embeddings.return_value = {'embedding': 'mock_embedding'}
        mock_load_models.return_value = mock_get_embeddings

        mock_llm = MagicMock()
        mock_llm.return_value = {'response': 'mock response'}
        mock_initialize_llm.return_value = mock_llm
        
        app = Flask(__name__)
        register_routes(app)
        
        client = app.test_client()

        # Test /update_embeddings route
        response = client.post('/update_embeddings', json={'content': 'mock content'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.get_json()['status'])

        # Test /chat route
        response = client.post('/chat', json={'query': 'mock query'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.get_json())

if __name__ == '__main__':
    unittest.main()
