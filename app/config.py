import os
import logging
from dotenv import load_dotenv

# Initialize the logger
logger = logging.getLogger(__name__)

def configure_app(app):
    """
    Configure the Flask application with settings from environment variables.

    Args:
        app (Flask): The Flask application instance to configure.
    """
    # Load environment variables from a .env file
    load_dotenv()
    logger.debug("Environment variables loaded from .env file.")

    # Set the MODEL_API_URL configuration from environment variable or default value
    app.config['MODEL_API_URL'] = os.getenv('MODEL_API_URL', "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2")
    logger.debug(f"MODEL_API_URL set to: {app.config['MODEL_API_URL']}")

    # Set the LLM_API_URL configuration from environment variable or default value
    app.config['LLM_API_URL'] = os.getenv('LLM_API_URL', "https://api-inference.huggingface.co/models/openai-community/gpt2")
    logger.debug(f"LLM_API_URL set to: {app.config['LLM_API_URL']}")

    # Retrieve the Hugging Face Hub token from environment variables
    hf_token = os.getenv('HUGGINGFACE_HUB_TOKEN')
    if hf_token:
        # Set the headers for API requests
        app.config['HEADERS'] = {"Authorization": f"Bearer {hf_token}"}
        logger.debug("Authorization header set with Hugging Face Hub token.")
    else:
        # Log an error and raise an exception if the token is not set
        logger.error("HUGGINGFACE_HUB_TOKEN environment variable not set.")
        raise ValueError("HUGGINGFACE_HUB_TOKEN environment variable not set")

    # Log the successful configuration of the application
    logger.info("Application configured successfully with environment variables.")