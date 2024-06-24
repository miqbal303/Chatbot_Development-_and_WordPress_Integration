<?php
/*
Plugin Name: RAG Chatbot Plugin
Description: A plugin to integrate the RAG Chatbot with WordPress.
Version: 1.0
Author: Mohammad Iqbal
*/

// Enqueue necessary scripts
function rag_chatbot_enqueue_scripts() {
    wp_enqueue_script('rag-chatbot-js', plugins_url('/js/rag-chatbot.js', __FILE__), array('jquery'), null, true);
    wp_localize_script('rag-chatbot-js', 'ragChatbot', array(
        'ajax_url' => admin_url('admin-ajax.php'),
    ));
}
add_action('wp_enqueue_scripts', 'rag_chatbot_enqueue_scripts');

// Handle AJAX requests for chatbot query
function rag_chatbot_handle_query() {
    $query = sanitize_text_field($_POST['query']);
    $context = isset($_POST['context']) ? array_map('sanitize_text_field', $_POST['context']) : array();

    $response = wp_remote_post('https://23e4-103-252-216-191.ngrok-free.app/chat', array(
        'body' => json_encode(array(
            'query' => $query,
            'context' => $context,
        )),
        'headers' => array(
            'Content-Type' => 'application/json',
        ),
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

// Handle AJAX requests for query suggestions
function rag_chatbot_suggest_query() {
    $query = sanitize_text_field($_POST['query']);
    $response = wp_remote_post('https://23e4-103-252-216-191.ngrok-free.app/suggest_query', array(
        'body' => json_encode(array(
            'query' => $query,
        )),
        'headers' => array(
            'Content-Type' => 'application/json',
        ),
    ));

    if (is_wp_error($response)) {
        error_log('Error in wp_remote_post: ' . $response->get_error_message());
        echo json_encode(array('error' => 'Internal Server Error'));
    } else {
        echo wp_remote_retrieve_body($response);
    }
    wp_die();
}
add_action('wp_ajax_rag_chatbot_suggest', 'rag_chatbot_suggest_query');
add_action('wp_ajax_nopriv_rag_chatbot_suggest', 'rag_chatbot_suggest_query');

// Define the shortcode function
function rag_chatbot_shortcode() {
    ob_start(); ?>
    <form id="rag-chatbot-form">
        <label for="query">Ask a question:</label>
        <input type="text" id="query" name="query" required>
        <div id="query-suggestions" style="border: 1px solid #ccc; max-height: 150px; overflow-y: auto;"></div>
        <label for="context">Context (optional):</label>
        <textarea id="context" name="context"></textarea>
        <button type="submit">Submit</button>
    </form>
    <div id="chatbot-response"></div>
    <?php
    return ob_get_clean();
}
add_shortcode('rag_chatbot', 'rag_chatbot_shortcode');
