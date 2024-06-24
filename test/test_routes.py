import unittest
from app import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_update_embeddings_no_content(self):
        response = self.client.post('/update_embeddings', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Content is required', response.get_json()['error'])

    def test_chat_no_query(self):
        response = self.client.post('/chat', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Query is required', response.get_json()['error'])
