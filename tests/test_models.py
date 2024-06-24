import unittest
from flask import Flask
from app.models import load_models

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['MODEL_ID'] = 'sentence-transformers/all-MiniLM-L6-v2'
        self.app.config['LLM_MODEL_ID'] = 'distilbert-base-uncased'
        self.app.config['EMBEDDING_DIM'] = 384

    def test_load_models(self):
        tokenizer, model, index = load_models(self.app)
        self.assertIsNotNone(tokenizer)
        self.assertIsNotNone(model)
        self.assertIsNotNone(index)
