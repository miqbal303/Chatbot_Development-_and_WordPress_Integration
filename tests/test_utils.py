import unittest
from unittest.mock import patch, MagicMock
from app.utils import rag_generate_response, process_query_with_chain_of_thought, develop_reasoning_steps, refine_response_based_on_thought_steps, fetch_wordpress_content, filter_relevant_content

class TestUtils(unittest.TestCase):
    @patch('app.pipeline.initialize_llm')  # Correct the mock target
    def test_rag_generate_response(self, mock_initialize_llm):
        mock_llm = MagicMock()
        mock_llm.return_value = [{'generated_text': 'mock response'}]
        mock_initialize_llm.return_value = mock_llm
        result = rag_generate_response('mock query', mock_llm)
        self.assertEqual(result, 'mock response')

    def test_develop_reasoning_steps(self):
        result = develop_reasoning_steps('initial response', ['context1', 'context2'])
        self.assertEqual(result, ['initial response', 'context1', 'context2'])

    def test_refine_response_based_on_thought_steps(self):
        result = refine_response_based_on_thought_steps(['step1', 'step2'])
        self.assertEqual(result, 'step1 step2')

    @patch('app.utils.requests.get')
    def test_fetch_wordpress_content(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'content': {'rendered': 'mock content'}}]
        mock_get.return_value = mock_response
        
        result = fetch_wordpress_content('mock query')
        self.assertIn('mock content', result)

    def test_filter_relevant_content(self):
        content = "This is a test content. It includes keywords for filtering."
        query = "keywords"
        result = filter_relevant_content(content, query)
        self.assertIn("It includes keywords for filtering.", result)

if __name__ == '__main__':
    unittest.main()
