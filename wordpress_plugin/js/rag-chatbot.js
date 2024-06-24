jQuery(document).ready(function($) {
    let typingTimer;                // Timer identifier
    let doneTypingInterval = 500;  // Time in ms, 500ms after user stops typing

    $('#query').on('keyup', function() {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(doneTyping, doneTypingInterval);
    });

    $('#query').on('keydown', function() {
        clearTimeout(typingTimer);
    });

    function doneTyping() {
        let query = $('#query').val();
        if (query.length > 2) {
            $.post(ragChatbot.ajax_url, {
                action: 'rag_chatbot_suggest_query',
                query: query
            }, function(response) {
                let suggestions = response.suggestions;
                $('#query-suggestions').empty();
                suggestions.forEach(suggestion => {
                    $('#query-suggestions').append('<div class="suggestion">' + suggestion + '</div>');
                });

                $('.suggestion').on('click', function() {
                    $('#query').val($(this).text());
                    $('#query-suggestions').empty();
                });
            });
        }
    }

    $('#rag-chatbot-form').on('submit', function(e) {
        e.preventDefault();
        var query = $('#query').val();
        var context = $('#context').val().split('\n');  // Assuming context is a textarea
        $.post(ragChatbot.ajax_url, {
            action: 'rag_chatbot_query',
            query: query,
            context: context
        }, function(response) {
            $('#chatbot-response').text(response);
        });
    });
});
