# Tests Directory

This directory contains unit tests for the RAG chatbot application. Each test file corresponds to a different module in the `app` directory.

## Test Files

- `__init__.py`: Marks the directory as a package.
- `test_config.py`: Tests configuration settings.
- `test_models.py`: Tests model loading.
- `test_pipeline.py`: Tests pipeline initialization.
- `test_routes.py`: Tests the API routes.
- `test_utils.py`: Tests utility functions.

## Running Tests

To run the tests, use the following command:
```bash
python -m unittest discover -s tests
