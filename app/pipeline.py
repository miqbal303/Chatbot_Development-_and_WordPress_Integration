import logging
from transformers import pipeline

logger = logging.getLogger(__name__)

def initialize_pipeline(model, tokenizer):
    try:
        llm = pipeline('text-generation', model=model, tokenizer=tokenizer, config={"temperature": 0.7, "max_new_tokens": 50, "top_k": 30})
        logger.info("Text generation pipeline initialized successfully.")
        return llm
    except Exception as e:
        logger.error(f"Error initializing text generation pipeline: {e}", exc_info=True)
        raise
