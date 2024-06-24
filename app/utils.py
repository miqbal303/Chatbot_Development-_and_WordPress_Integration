import logging
import requests

logger = logging.getLogger(__name__)

def process_query_with_chain_of_thought(user_query, previous_context, llm):
    try:
        initial_response = rag_generate_response(user_query, llm)
        logger.debug(f"Initial response: {initial_response}")

        thought_steps = develop_reasoning_steps(initial_response, previous_context)
        logger.debug(f"Thought steps: {thought_steps}")

        final_response = refine_response_based_on_thought_steps(thought_steps)
        logger.info(f"Final response: {final_response}")
        return final_response
    except Exception as e:
        logger.error(f"Error in process_query_with_chain_of_thought: {e}", exc_info=True)
        return "An error occurred while processing the query."

def rag_generate_response(user_query, llm):
    try:
        response = llm(user_query, max_new_tokens=50)
        logger.debug(f"LLM response: {response}")

        if isinstance(response, list) and len(response) > 0:
            generated_text = response[0]['generated_text']
            logger.info(f"Generated response for query: {user_query}")
            return generated_text
        else:
            logger.error("Unexpected response format from LLM")
            return "An error occurred while generating the response."
    except Exception as e:
        logger.error(f"Error in rag_generate_response: {e}", exc_info=True)
        return "An error occurred while generating the response."

def develop_reasoning_steps(initial_response, previous_context):
    thought_steps = [initial_response] + previous_context
    logger.info(f"Developed reasoning steps: {thought_steps}")
    return thought_steps

def refine_response_based_on_thought_steps(thought_steps):
    final_response = " ".join(thought_steps)
    logger.info(f"Refined final response: {final_response}")
    return final_response


def fetch_wordpress_content(query):
    # Replace with the actual URL of your WordPress site and REST API endpoint
    wordpress_api_url = "http://rag.local/wp-json/wp/v2/posts"
    response = requests.get(wordpress_api_url, params={"search": query})

    if response.status_code == 200:
        posts = response.json()
        if posts:
            return posts[0]['content']['rendered']
        else:
            return "No relevant posts found."
    else:
        return "Failed to fetch content from WordPress."
