from flask import request, jsonify, Blueprint
from app.models import load_models
from app.pipeline import initialize_llm
from app.utils import process_query_with_chain_of_thought, fetch_wordpress_content, rag_generate_response, develop_reasoning_steps, refine_response_based_on_thought_steps, filter_relevant_content
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

def register_routes(app):
    """
    Register routes for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    # Create a Blueprint for the main routes
    main = Blueprint('main', __name__)
    
    # Load models and initialize the LLM
    get_embeddings = load_models(app)
    llm = initialize_llm(app)

    @main.route('/update_embeddings', methods=['POST'])
    def update_embeddings():
        """
        Route to update embeddings for a given text.

        Returns:
            JSON response with the status and embeddings or an error message.
        """
        try:
            # Get the JSON data from the request
            post = request.json
            text = post.get('content')
            if not text:
                logger.warning("No content provided in the request.")
                return jsonify({"error": "Content is required"}), 400

            # Get embeddings for the provided text
            embeddings = get_embeddings(text)
            logger.info(f"Updated embeddings for text: {text}")
            return jsonify({"status": "success", "embeddings": embeddings})
        except Exception as e:
            logger.error(f"Error in /update_embeddings route: {e}", exc_info=True)
            return jsonify({"error": "Internal Server Error"}), 500

    @main.route('/chat', methods=['POST'])
    def chat():
        """
        Route to handle chat queries.

        Returns:
            JSON response with the generated response or an error message.
        """
        try:
            # Get the JSON data from the request
            data = request.json
            user_query = data.get('query')
            if not user_query:
                logger.warning("No query provided in the request.")
                return jsonify({"error": "Query is required"}), 400

            previous_context = data.get('context', [])

            # Fetch WordPress content based on the user query
            wp_content = fetch_wordpress_content(user_query)
            logger.debug(f"Fetched WordPress content: {wp_content}")

            # Generate initial response using the LLM
            initial_response = rag_generate_response(user_query, llm)
            logger.debug(f"Initial LLM response: {initial_response}")

            # Develop reasoning steps based on the initial response and previous context
            thought_steps = develop_reasoning_steps(initial_response, previous_context + [wp_content])
            logger.debug(f"Developed thought steps: {thought_steps}")

            # Refine the final response based on the thought steps
            final_response = refine_response_based_on_thought_steps(thought_steps)
            logger.info(f"Final response: {final_response}")

            # Process the query with chain of thought
            response = process_query_with_chain_of_thought(user_query, previous_context + [wp_content], llm)
            logger.info(f"Processed response with chain of thought: {response}")

            return jsonify({"response": response})
        except Exception as e:
            logger.error(f"Error in /chat route: {e}", exc_info=True)
            return jsonify({"error": "Internal Server Error"}), 500

    # Register the Blueprint with the Flask application
    app.register_blueprint(main)