import unittest
from unittest.mock import patch
from flask import Flask
from app.config import configure_app

class TestConfig(unittest.TestCase):
    @patch('app.config.os.getenv')
    @patch('app.config.load_dotenv')
    def test_configure_app(self, mock_load_dotenv, mock_getenv):
        mock_getenv.side_effect = lambda key, default=None: {
            'MODEL_API_URL': 'https://mockmodelapi.url',
            'LLM_API_URL': 'https://mockllmapi.url',
            'HUGGINGFACE_HUB_TOKEN': 'mocktoken'
        }.get(key, default)
        
        app = Flask(__name__)
        configure_app(app)
        
        self.assertEqual(app.config['MODEL_API_URL'], 'https://mockmodelapi.url')
        self.assertEqual(app.config['LLM_API_URL'], 'https://mockllmapi.url')
        self.assertEqual(app.config['HEADERS'], {'Authorization': 'Bearer mocktoken'})

if __name__ == '__main__':
    unittest.main()
