import unittest
from app.utils import process_query_with_chain_of_thought

class TestUtils(unittest.TestCase):
    def test_process_query_with_chain_of_thought(self):
        user_query = "What is AI?"
        previous_context = ["AI stands for Artificial Intelligence."]
        llm = lambda x, max_new_tokens: [{"generated_text": "AI is the simulation of human intelligence by machines."}]
        response = process_query_with_chain_of_thought(user_query, previous_context, llm)
        self.assertIn("AI is the simulation of human intelligence by machines.", response)
