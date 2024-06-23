import logging
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModel, pipeline
import faiss
import os
import numpy as np

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for verbose logging
logger = logging.getLogger(__name__)

# Flask app initialization
app = Flask(__name__)

# Load configurations from environment variables or default values
MODEL_ID = os.getenv('MODEL_ID', 'sentence-transformers/all-MiniLM-L6-v2')
LLM_MODEL_ID = os.getenv('LLM_MODEL_ID', 'distilbert-base-uncased')  # Use a lightweight model

try:
    EMBEDDING_DIM = int(os.getenv('EMBEDDING_DIM', 384))
except ValueError:
    EMBEDDING_DIM = 384
    logger.warning("Invalid EMBEDDING_DIM provided, defaulting to 384")

logger.debug("Starting application initialization...")

# Initialize tokenizer and model using transformers
try:
    logger.debug(f"Loading tokenizer and model '{MODEL_ID}'...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModel.from_pretrained(LLM_MODEL_ID)
    logger.info(f"Tokenizer and model '{MODEL_ID}' loaded successfully.")
except Exception as e:
    logger.error(f"Error loading tokenizer and model '{MODEL_ID}': {e}", exc_info=True)
    raise

# Initialize FAISS index
try:
    logger.debug(f"Initializing FAISS index with dimension {EMBEDDING_DIM}...")
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    logger.info("FAISS index initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing FAISS index: {e}", exc_info=True)
    raise

# Initialize HuggingFacePipeline for text generation
try:
    logger.debug(f"Initializing text generation pipeline for model '{LLM_MODEL_ID}'...")
    llm = pipeline('text-generation', model=model, tokenizer=tokenizer, config={"temperature": 0.7, "max_new_tokens": 50, "top_k": 30})
    logger.info(f"Text generation pipeline for model '{LLM_MODEL_ID}' initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing text generation pipeline for model '{LLM_MODEL_ID}': {e}", exc_info=True)
    raise

logger.debug("Application initialization complete.")

@app.route('/update_embeddings', methods=['POST'])
def update_embeddings():
    """Endpoint to update embeddings for new content."""
    try:
        post = request.json
        text = post.get('content')
        if not text:
            logger.warning("No content provided in the request.")
            return jsonify({"error": "Content is required"}), 400

        # Generate embeddings for the provided text
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()

        # Add the embeddings to the FAISS index
        index.add(embeddings)
        logger.info(f"Updated embeddings for text: {text}")
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error in /update_embeddings route: {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint to handle chat interactions."""
    try:
        data = request.json
        user_query = data.get('query')
        if not user_query:
            logger.warning("No query provided in the request.")
            return jsonify({"error": "Query is required"}), 400

        previous_context = data.get('context', [])
        response = process_query_with_chain_of_thought(user_query, previous_context)
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error in /chat route: {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

def process_query_with_chain_of_thought(user_query, previous_context):
    """Process the user query with Chain of Thought strategy."""
    try:
        # Generate initial response using RAG
        initial_response = rag_generate_response(user_query)
        logger.debug(f"Initial response: {initial_response}")

        # Develop reasoning steps based on the initial response and previous context
        thought_steps = develop_reasoning_steps(initial_response, previous_context)
        logger.debug(f"Thought steps: {thought_steps}")

        # Refine the response based on the reasoning steps
        final_response = refine_response_based_on_thought_steps(thought_steps)
        logger.info(f"Final response: {final_response}")
        return final_response
    except Exception as e:
        logger.error(f"Error in process_query_with_chain_of_thought: {e}", exc_info=True)
        return "An error occurred while processing the query."

def rag_generate_response(user_query):
    """Generate a response using RAG model."""
    try:
        response = llm(user_query, max_new_tokens=50)  # Ensure max_new_tokens is set
        logger.debug(f"LLM response: {response}")

        if isinstance(response, list) and len(response) > 0:
            generated_text = response[0]['generated_text']
            logger.info(f"Generated response for query: {user_query}")
            return generated_text
        else:
            logger.error("Unexpected response format from LLM")
            return "An error occurred while generating the response."
    except Exception as e:
        logger.error(f"Error in rag_generate_response: {e}", exc_info=True)
        return "An error occurred while generating the response."

def develop_reasoning_steps(initial_response, previous_context):
    """Develop reasoning steps for the Chain of Thought."""
    thought_steps = [initial_response] + previous_context
    logger.info(f"Developed reasoning steps: {thought_steps}")
    return thought_steps

def refine_response_based_on_thought_steps(thought_steps):
    """Refine the final response based on reasoning steps."""
    final_response = " ".join(thought_steps)
    logger.info(f"Refined final response: {final_response}")
    return final_response

if __name__ == '__main__':
    try:
        logger.debug("Starting Flask app...")
        app.run(debug=False)
    except Exception as e:
        logger.error(f"Error running Flask app: {e}", exc_info=True)