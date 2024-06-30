import unittest
from unittest.mock import patch
from app import create_app

class TestInit(unittest.TestCase):
    @patch('app.config.configure_app')
    @patch('app.routes.register_routes')
    @patch('app.models.load_models')
    def test_create_app(self, mock_load_models, mock_register_routes, mock_configure_app):
        app = create_app()
        self.assertIsNotNone(app)
        mock_configure_app.assert_called_once()
        mock_register_routes.assert_called_once()
        mock_load_models.assert_called_once()

if __name__ == '__main__':
    unittest.main()
