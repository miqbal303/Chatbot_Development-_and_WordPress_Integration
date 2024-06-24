import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
import faiss

logger = logging.getLogger(__name__)

def load_models(app):
    model_id = app.config['MODEL_ID']
    llm_model_id = app.config['LLM_MODEL_ID']
    embedding_dim = app.config['EMBEDDING_DIM']

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(llm_model_id)
        logger.info(f"Tokenizer and model '{model_id}' loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading tokenizer and model '{model_id}': {e}", exc_info=True)
        raise

    try:
        index = faiss.IndexFlatL2(embedding_dim)
        logger.info("FAISS index initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing FAISS index: {e}", exc_info=True)
        raise

    return tokenizer, model, index
