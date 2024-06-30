import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.pipeline import initialize_llm

class TestPipeline(unittest.TestCase):
    @patch('app.pipeline.requests.post')
    def test_call_llm(self, mock_post):
        app = Flask(__name__)
        app.config['HEADERS'] = {'Authorization': 'Bearer mocktoken'}
        app.config['LLM_API_URL'] = 'https://mockllmapi.url'
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'generated_text': 'mock response'}
        mock_post.return_value = mock_response
        
        llm = initialize_llm(app)
        result = llm('mock input')
        
        self.assertEqual(result, {'generated_text': 'mock response'})
        mock_post.assert_called_once_with(
            'https://mockllmapi.url',
            headers={'Authorization': 'Bearer mocktoken'},
            json={'inputs': 'mock input'}
        )

if __name__ == '__main__':
    unittest.main()
