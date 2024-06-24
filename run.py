from app import create_app
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        logger.debug("Starting Flask app...")
        app = create_app()
        app.run(debug=False)
    except Exception as e:
        logger.error(f"Error running Flask app: {e}", exc_info=True)
