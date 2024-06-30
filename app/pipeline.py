import logging
import requests

# Initialize the logger
logger = logging.getLogger(__name__)

def initialize_llm(app):
    """
    Initialize the LLM (Language Model) by setting up a function to call the LLM API.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        function: A function to call the LLM API with given inputs.
    """
    # Retrieve the LLM API URL and headers from the app configuration
    api_url = app.config['LLM_API_URL']
    headers = app.config['HEADERS']
    logger.debug(f"LLM API URL: {api_url}")
    logger.debug(f"Headers: {headers}")

    def call_llm(inputs):
        """
        Call the LLM API with the given inputs.

        Args:
            inputs (str): The input text to generate a response for.

        Returns:
            dict: The JSON response from the LLM API.
        """
        # Prepare the payload for the API request
        payload = {"inputs": inputs}
        logger.debug(f"Payload for LLM API: {payload}")

        # Make a POST request to the LLM API
        response = requests.post(api_url, headers=headers, json=payload)
        logger.debug(f"Response from LLM API: {response.status_code} {response.text}")

        # Check if the response status code indicates success
        if response.status_code == 200:
            logger.info("Successfully generated response from LLM API.")
            return response.json()
        else:
            # Log an error message with the response content
            logger.error(f"Error calling LLM API: {response.text}")
            return {"error": "Failed to generate response"}

    return call_llm