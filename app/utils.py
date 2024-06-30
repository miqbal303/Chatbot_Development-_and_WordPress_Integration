import logging
import requests

# Initialize the logger
logger = logging.getLogger(__name__)

def filter_relevant_content(content, query):
    """
    Filter the relevant content based on the query.

    Args:
        content (str): The content to be filtered.
        query (str): The search query.

    Returns:
        str: The filtered content.
    """
    # Simple keyword-based filtering
    keywords = query.split()
    filtered_content = []
    for line in content.split('\n'):
        if any(keyword.lower() in line.lower() for keyword in keywords):
            filtered_content.append(line)
    return '\n'.join(filtered_content)


def fetch_wordpress_content(query):
    """
    Fetch content from WordPress based on the query.

    Args:
        query (str): The search query.

    Returns:
        str: The fetched content or an error message.
    """
    wordpress_post_api_url = "https://eliminatechannel.s3-tastewp.com/wp-json/wp/v2/posts"
    wordpress_page_api_url = "https://eliminatechannel.s3-tastewp.com/wp-json/wp/v2/pages"

    # Fetch posts
    post_response = requests.get(wordpress_post_api_url, params={"search": query})
    logger.debug(f"WordPress Posts API URL: {wordpress_post_api_url}")
    logger.debug(f"Query: {query}")
    logger.debug(f"Post Response Status Code: {post_response.status_code}")
    logger.debug(f"Post Response Text: {post_response.text}")

    posts_content = ""
    if post_response.status_code == 200:
        posts = post_response.json()
        if posts:
            posts_content = posts[0]['content']['rendered']
            posts_content = filter_relevant_content(posts_content, query)
        else:
            posts_content = "No relevant posts found."
    else:
        logger.error(f"Failed to fetch posts from WordPress: {post_response.text}")
        posts_content = "Failed to fetch posts from WordPress."

    # Fetch pages
    page_response = requests.get(wordpress_page_api_url, params={"search": query})
    logger.debug(f"WordPress Pages API URL: {wordpress_page_api_url}")
    logger.debug(f"Query: {query}")
    logger.debug(f"Page Response Status Code: {page_response.status_code}")
    logger.debug(f"Page Response Text: {page_response.text}")

    pages_content = ""
    if page_response.status_code == 200:
        pages = page_response.json()
        if pages:
            pages_content = pages[0]['content']['rendered']
            pages_content = filter_relevant_content(pages_content, query)
        else:
            pages_content = "No relevant pages found."
    else:
        logger.error(f"Failed to fetch pages from WordPress: {page_response.text}")
        pages_content = "Failed to fetch pages from WordPress."

    return f"Posts: {posts_content}\n\nPages: {pages_content}"

def rag_generate_response(user_query, llm):
    """
    Generate a response using the provided language model (LLM).

    Args:
        user_query (str): The user's query.
        llm (callable): The language model function.

    Returns:
        str: The generated response or an error message.
    """
    try:
        # Generate response using the LLM
        response = llm(user_query)
        logger.debug(f"LLM response: {response}")

        # Check if the response format is as expected
        if isinstance(response, list) and 'generated_text' in response[0]:
            generated_text = response[0]['generated_text']
            logger.info(f"Generated response for query: {user_query}")
            return generated_text
        else:
            logger.error("Unexpected response format from LLM")
            return "An error occurred while generating the response."
    except Exception as e:
        logger.error(f"Error in rag_generate_response: {e}", exc_info=True)
        return "An error occurred while generating the response."

def process_query_with_chain_of_thought(user_query, previous_context, llm):
    """
    Process the user's query using a chain of thought approach.

    Args:
        user_query (str): The user's query.
        previous_context (list): The previous context.
        llm (callable): The language model function.

    Returns:
        str: The final response or an error message.
    """
    try:
        # Generate initial response
        initial_response = rag_generate_response(user_query, llm)
        logger.debug(f"Initial response: {initial_response}")

        # Develop reasoning steps
        thought_steps = develop_reasoning_steps(initial_response, previous_context)
        logger.debug(f"Thought steps: {thought_steps}")

        # Refine the final response based on thought steps
        final_response = refine_response_based_on_thought_steps(thought_steps)
        logger.info(f"Final response: {final_response}")
        return final_response
    except Exception as e:
        logger.error(f"Error in process_query_with_chain_of_thought: {e}", exc_info=True)
        return "An error occurred while processing the query."

def develop_reasoning_steps(initial_response, previous_context):
    """
    Develop reasoning steps based on the initial response and previous context.

    Args:
        initial_response (str): The initial response.
        previous_context (list): The previous context.

    Returns:
        list: The developed reasoning steps.
    """
    thought_steps = [initial_response] + previous_context
    logger.info(f"Developed reasoning steps: {thought_steps}")
    return thought_steps

def refine_response_based_on_thought_steps(thought_steps):
    """
    Refine the final response based on the developed thought steps.

    Args:
        thought_steps (list): The developed thought steps.

    Returns:
        str: The refined final response.
    """
    final_response = " ".join(thought_steps)
    logger.info(f"Refined final response: {final_response}")
    return final_response