import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.models import load_models

class TestModels(unittest.TestCase):
    @patch('app.models.requests.post')
    def test_get_embeddings(self, mock_post):
        app = Flask(__name__)
        app.config['HEADERS'] = {'Authorization': 'Bearer mocktoken'}
        app.config['MODEL_API_URL'] = 'https://mockmodelapi.url'
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'embedding': 'mock_embedding'}
        mock_post.return_value = mock_response
        
        get_embeddings = load_models(app)
        result = get_embeddings('mock text')
        
        self.assertEqual(result, {'embedding': 'mock_embedding'})
        mock_post.assert_called_once_with(
            'https://mockmodelapi.url',
            headers={'Authorization': 'Bearer mocktoken'},
            json={'inputs': 'mock text'}
        )

if __name__ == '__main__':
    unittest.main()
