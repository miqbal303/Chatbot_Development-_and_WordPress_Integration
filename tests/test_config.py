import unittest
from app import create_app
from app.config import configure_app

class TestConfig(unittest.TestCase):
    def test_default_config(self):
        app = create_app()
        configure_app(app)
        self.assertEqual(app.config['MODEL_ID'], 'sentence-transformers/all-MiniLM-L6-v2')
        self.assertEqual(app.config['LLM_MODEL_ID'], 'gpt2')
        self.assertEqual(app.config['EMBEDDING_DIM'], 384)

if __name__ == '__main__':
    unittest.main()
