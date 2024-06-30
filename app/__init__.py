import logging
from flask import Flask
from app.config import configure_app
from app.routes import register_routes
from app.models import load_models

# Initialize the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    # Create a new Flask application instance
    application = Flask(__name__)
    app = application

    # Log the creation of the Flask application
    logger.debug("Flask application instance created.")

    # Configure the application using the settings from app.config
    configure_app(app)
    logger.debug("Application configured with settings from app.config.")

    # Register the routes for the application
    register_routes(app)
    logger.debug("Routes registered for the application.")

    # Load models and set up the function to get embeddings
    load_models(app)
    logger.debug("Models loaded and embeddings function set up.")

    # Log the successful creation of the application
    logger.info("Flask application created and configured successfully.")

    return app