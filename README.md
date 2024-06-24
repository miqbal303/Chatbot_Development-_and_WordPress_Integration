# **Objective** : 

Develop a versatile, intelligent chatbot that utilizes a Retrieval-Augmented Generation (RAG) system enhanced with a Chain of Thought (CoT) strategy. This chatbot will be integrated into various WordPress blogs and sites, designed to handle and adapt to a wide range of topics, maintaining logical and contextually relevant interactions.

## Setup Instructions

1. **Create Virtual Environment**:
    ```bash
    conda create -p venv python==3.10 -y && conda activate venv\
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```


3. **Run the Application**:
    ```bash
    python run.py
    ```

## WordPress Integration

The project includes a WordPress plugin to integrate the chatbot.

### Plugin Files

- `rag-chatbot-plugin.php`: Main plugin file.
- `js/rag-chatbot.js`: JavaScript for handling AJAX requests and suggestions.

### Installation

1. Copy the plugin files to your WordPress `wp-content/plugins` directory.
2. Activate the plugin from the WordPress admin dashboard.
3. Use the `[rag_chatbot]` shortcode to add the chatbot to a page.

## Running Tests

To run all tests, use:
```bash
python -m unittest discover -s tests

