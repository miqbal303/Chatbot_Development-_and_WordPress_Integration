# App Directory

This directory contains the main application logic for the RAG (Retrieve and Generate) chatbot. The structure and purpose of each file are as follows:

- `__init__.py`: Initializes the Flask application.
- `config.py`: Configures the application settings.
- `models.py`: Handles the loading of models
- `pipeline.py`: Initializes the text generation pipeline.
- `routes.py`: Defines the API routes for the chatbot.
- `utils.py`: Contains utility functions for processing queries and fetching WordPress content.

## Setup and Usage

1. **Initialize the Flask App**: 
    ```python
    from app import create_app

    app = create_app()
    app.run()
    ```

2. **Configuration**:
    Set environment variables to configure the app:
    ```bash
    export MODEL_ID='your-model-id'
    export LLM_MODEL_ID='your-llm-model-id'
    export EMBEDDING_DIM=384
    ```

3. **Running the App**:
    ```bash
    python run.py
    ```

## API Endpoints

- `POST /update_embeddings`: Updates the FAISS index with embeddings of the provided content.
- `POST /chat`: Handles chat queries and provides responses.

## Utility Functions

- `process_query_with_chain_of_thought`: Processes user queries with the chatbot.
- `fetch_wordpress_content`: Fetches content from a WordPress site based on the query.
