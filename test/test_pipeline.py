import unittest
from unittest.mock import patch, MagicMock
from app.pipeline import initialize_pipeline

class TestPipeline(unittest.TestCase):
    @patch('app.pipeline.pipeline')
    def test_initialize_pipeline(self, mock_pipeline):
        mock_llm = MagicMock()
        mock_pipeline.return_value = mock_llm
        
        model = MagicMock()
        tokenizer = MagicMock()
        
        llm = initialize_pipeline(model, tokenizer)
        
        mock_pipeline.assert_called_once_with(
            'text-generation',
            model=model,
            tokenizer=tokenizer,
            config={"temperature": 0.7, "max_new_tokens": 50, "top_k": 30}
        )
        self.assertIsNotNone(llm)

if __name__ == '__main__':
    unittest.main()
