from flask import request, jsonify
from app.models import load_models
from app.pipeline import initialize_pipeline
from app.utils import process_query_with_chain_of_thought, fetch_wordpress_content
import logging

logger = logging.getLogger(__name__)

def register_routes(app):
    tokenizer, model, index = load_models(app)
    llm = initialize_pipeline(model, tokenizer)

    @app.route('/update_embeddings', methods=['POST'])
    def update_embeddings():
        try:
            post = request.json
            text = post.get('content')
            if not text:
                logger.warning("No content provided in the request.")
                return jsonify({"error": "Content is required"}), 400

            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()

            index.add(embeddings)
            logger.info(f"Updated embeddings for text: {text}")
            return jsonify({"status": "success"})
        except Exception as e:
            logger.error(f"Error in /update_embeddings route: {e}", exc_info=True)
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/chat', methods=['POST'])
    def chat():
        try:
            data = request.json
            user_query = data.get('query')
            if not user_query:
                logger.warning("No query provided in the request.")
                return jsonify({"error": "Query is required"}), 400

            previous_context = data.get('context', [])
            # Fetch content from WordPress based on the user query
            wp_content = fetch_wordpress_content(user_query)
            
            # Process the query with the chatbot and include fetched content
            response = process_query_with_chain_of_thought(user_query, previous_context + [wp_content], llm)
            return jsonify({"response": response})
        except Exception as e:
            logger.error(f"Error in /chat route: {e}", exc_info=True)
            return jsonify({"error": "Internal Server Error"}), 500
