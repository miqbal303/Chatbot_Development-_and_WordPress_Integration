jQuery(document).ready(function($) {
    $('#rag-chatbot-form').on('submit', function(e) {
        e.preventDefault();
        var query = $('#query').val();
        var context = $('#context').val() ? $('#context').val().split('\n') : [];
        var nonce = $('#rag_chatbot_nonce').val();

        $.post(ragChatbot.ajax_url, {
            action: 'rag_chatbot_query',
            query: query,
            context: context,
            nonce: nonce
        }, function(response) {
            // Parse JSON response if necessary
            try {
                response = JSON.parse(response);
            } catch (e) {
                console.error("Failed to parse JSON response:", e);
            }

            if (response.error) {
                $('#chatbot-response').html(response.error);
            } else {
                $('#chatbot-response').html(response.response);
            }
        }).fail(function(xhr, status, error) {
            console.error("An error occurred while processing your request:", error, xhr.responseText);
            $('#chatbot-response').html("An error occurred while processing your request.");
        });
    });
});
