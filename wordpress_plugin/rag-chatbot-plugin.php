<?php
/*
Plugin Name: RAG Chatbot Plugin
Description: A plugin to integrate the RAG Chatbot with WordPress.
Version: 1.0
Author: Mohammad Iqbal
*/

// Enqueue necessary scripts and styles
function rag_chatbot_enqueue_scripts() {
    wp_enqueue_script('rag-chatbot-js', plugins_url('/js/rag_chatbot.js', __FILE__), array('jquery'), null, true);
    wp_enqueue_style('rag-chatbot-css', plugins_url('/css/rag_chatbot.css', __FILE__));
    wp_localize_script('rag-chatbot-js', 'ragChatbot', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('rag_chatbot_nonce')
    ));
}
add_action('wp_enqueue_scripts', 'rag_chatbot_enqueue_scripts');

// Handle AJAX requests for chatbot query
function rag_chatbot_handle_query() {
    check_ajax_referer('rag_chatbot_nonce', 'nonce');

    $query = sanitize_text_field($_POST['query']);
    $context = isset($_POST['context']) ? array_map('sanitize_text_field', $_POST['context']) : array();

    $response = wp_remote_post('https://4db1-150-129-237-146.ngrok-free.app/chat', array(
        'body' => json_encode(array(
            'query' => $query,
            'context' => $context,
        )),
        'headers' => array(
            'Content-Type' => 'application/json',
        ),
        'timeout' => 120, // Increase the timeout to 120 seconds or more
    ));

    if (is_wp_error($response)) {
        error_log('Error in wp_remote_post: ' . $response->get_error_message());
        echo json_encode(array('error' => 'Internal Server Error'));
    } else {
        echo wp_remote_retrieve_body($response);
    }
    wp_die();
}
add_action('wp_ajax_rag_chatbot_query', 'rag_chatbot_handle_query');
add_action('wp_ajax_nopriv_rag_chatbot_query', 'rag_chatbot_handle_query');

// Define the shortcode function
function rag_chatbot_shortcode() {
    ob_start(); ?>
    <form id="rag-chatbot-form">
        <label for="query">Ask a question:</label>
        <input type="text" id="query" name="query" required>
        <label for="context">Context (optional):</label>
        <textarea id="context" name="context"></textarea>
        <input type="hidden" id="rag_chatbot_nonce" name="rag_chatbot_nonce" value="<?php echo wp_create_nonce('rag_chatbot_nonce'); ?>">
        <button type="submit">Submit</button>
    </form>
    <div id="chatbot-response"></div>
    <?php
    return ob_get_clean();
}
add_shortcode('rag_chatbot', 'rag_chatbot_shortcode');
?>
