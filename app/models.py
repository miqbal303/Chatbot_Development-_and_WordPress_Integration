import logging
import requests

# Initialize the logger
logger = logging.getLogger(__name__)

def load_models(app):
    """
    Load models by setting up a function to get embeddings from a model API.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        function: A function to get embeddings for a given text.
    """
    # Retrieve the headers and model API URL from the app configuration
    headers = app.config['HEADERS']
    model_api_url = app.config['MODEL_API_URL']

    def get_embeddings(text):
        """
        Get embeddings for a given text by calling the model API.

        Args:
            text (str): The input text to get embeddings for.

        Returns:
            dict: The JSON response from the model API containing embeddings.

        Raises:
            Exception: If the API call fails.
        """
        # Prepare the payload for the API request
        payload = {"inputs": text}
        logger.debug(f"Payload for model API: {payload}")

        # Make a POST request to the model API
        response = requests.post(model_api_url, headers=headers, json=payload)
        logger.debug(f"Response from model API: {response.status_code} {response.text}")

        # Check if the response status code indicates success
        if response.status_code == 200:
            logger.info("Successfully retrieved embeddings from model API.")
            return response.json()
        else:
            # Log an error message with the response content
            logger.error(f"Error calling model API: {response.text}")
            raise Exception("Failed to get embeddings")

    return get_embeddings