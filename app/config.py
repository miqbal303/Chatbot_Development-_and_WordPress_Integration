import os

def configure_app(app):
    app.config['MODEL_ID'] = os.getenv('MODEL_ID', 'sentence-transformers/all-MiniLM-L6-v2')
    app.config['LLM_MODEL_ID'] = os.getenv('LLM_MODEL_ID', 'EleutherAI/gpt-neo-125M')  # This is for text generation
    try:
        app.config['EMBEDDING_DIM'] = int(os.getenv('EMBEDDING_DIM', 384))
    except ValueError:
        app.config['EMBEDDING_DIM'] = 384
